import polars as pl 
from confluent_kafka import Consumer, KafkaError
import json 
import time
import asyncio 
import websockets 

connected_clients = set()

async def broadcast_to_clients(data):
    global connected_clients
    if connected_clients:
        message = json.dumps(data)
        disconnected = set() 
        for client in connected_clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
                
        connected_clients -= disconnected
        

        
async def websocket_handler(websocket, path):
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)
        
        

def refugee_analytics(df):
    analytics_df =  df.group_by("camp").agg([
        # Basic demographics
        pl.count().alias("total_households"),
        pl.col("householdSize").sum().alias("total_people"),
        pl.col("sex").filter(pl.col("sex") == "Male").count().alias("male_headed"),
        pl.col("sex").filter(pl.col("sex") == "Female").count().alias("female_headed"),
        
        # Protection needs - INFANTS
        pl.col("numOfInfants").sum().alias("total_infants"),
        pl.col("householdHasInfants").sum().alias("households_with_infants"),
        
        # Protection needs - ELDERLY
        pl.col("numOfElderly").sum().alias("total_elderly"),
        pl.col("householdHasElderly").sum().alias("households_with_elderly"),
        
        # Protection needs - DISABILITIES
        pl.col("householdHasDisability").sum().alias("households_with_disabilities"),
        pl.col("disabilityType").filter(pl.col("disabilityType").is_not_null()).unique().alias("disability_types"),
        
        # Legal protection - DOCUMENTATION
        pl.col("hasDocumentation").sum().alias("households_with_docs"),
        (pl.col("hasDocumentation").count() - pl.col("hasDocumentation").sum()).alias("households_without_docs"),
        pl.col("documentationType").filter(pl.col("documentationType").is_not_null()).unique().alias("doc_types_present"),
        
        # Additional metrics
        pl.col("householdSize").mean().alias("avg_household_size"),
        pl.col("householdSize").max().alias("max_household_size"),
        pl.col("ethnicity").unique().alias("ethnicities_present"),
        pl.col("religion").unique().alias("religions_present")
    ])
    
    return analytics_df.to_dicts()


async def main_async():
    print("Starting Polars refugee analytics...")
    
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'polars_consumers',
        'auto.offset.reset': 'latest'
    }
    
    consumer = Consumer(conf)
    
    consumer.subscribe(['refugee-registrations'])
    
    buffer = []
    
    try:
        
        websocket_server = await websockets.serve(websocket_handler, "localhost", 8765)
        print("WebSocket server started on ws://localhost:8765")
        
        while True:
            msg = consumer.poll(1.0)
            
            if msg and not msg.error():
                refugee_data = json.loads(msg.value().decode('utf-8'))
                buffer.append(refugee_data)
            
                if len(buffer) >=10:
                    df = pl.DataFrame(buffer)
                    analytics_data = refugee_analytics(df)
                    print("📊 Current Analytics:")
                    print(json.dumps(analytics_data, indent=2))
                    print("-" * 50)
                    
                    await broadcast_to_clients({
                        "timestamp": time.time(),
                        "analytics": analytics_data
                    })
                    buffer = []

            await asyncio.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n🛑 Analytics stopped by user")
        
    finally:
        consumer.close()
        websocket_server.close()
        await websocket_server.wait_closed()


        
def main():
    asyncio.run(main_async())
    
    
if __name__ == "__main__":
    main()
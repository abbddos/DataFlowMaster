from confluent_kafka import Producer 
import requests 
import json
import time 
import sys 

KAFKA_CONFIG = {'bootstrap.servers': 'localhost:9092'}
TOPIC = 'refugee-registrations'
producer = Producer(**KAFKA_CONFIG)


def delivery_report(err, msg):
    if err:
        print(f'❌ Failed: {err}')
    else:
        print(f'✅ Produced to {msg.topic()}')
        
        

def FetchData(page, per_page):
    try:
        API_URL = f'http://localhost:5000/api/v1/RefugeeRegistrations?page={page}&per_page={per_page}&_t={int(time.time())}'
        response = requests.get(API_URL)
        if response.status_code == 200:
                data = response.json()
                refugees = data['refugees']
                
                if refugees:
                    for refugee in refugees:
                        producer.produce(
                            TOPIC, 
                            key = f"Batch_{page}",
                            value = json.dumps(refugee),
                            callback=delivery_report
                        )
                        producer.poll(0)
                    records_count = len(refugees)
                    print(f"📨 Sent page {page} with {len(refugees)} refugees")
                    return records_count
                    
                else:
                    print("⏳ No new refugees - waiting...")
                    return 0
            
        else:
            print(f"❌ API error: {response.status_code}")
            return 0
        
    except Exception as e:
        print(str(e))
        return 0

    
    
    
if __name__ == "__main__":   
    page = 1
    per_page = 50


    while True:
        try:
            records_processed = FetchData(page, per_page)
            if records_processed >= per_page:
                page +=1
                
            time.sleep(5)
    
        except KeyboardInterrupt:
            print("\n🛑 Generator stopped by user")
            sys.exit(0)
            
        finally:
            producer.flush()
"""
Kafka Event Streaming Utilities
Because events are the lifeblood of microservices, bro!
"""
import os
import json
import logging
from typing import Dict, Any, Optional
from confluent_kafka import Producer, Consumer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic

logger = logging.getLogger(__name__)

class KafkaProducerBro:
    """The coolest Kafka producer this side of Silicon Valley"""
    
    def __init__(self):
        self.config = {
            'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP", "localhost:9092"),
            'client.id': f"n3xtpath-{os.getenv('SERVICE_NAME', 'unknown')}"
        }
        self.producer = Producer(self.config)
    
    def send_event(self, topic: str, key: str, value: Dict[str, Any]) -> bool:
        """Send an event like a boss"""
        try:
            message = json.dumps(value) if isinstance(value, dict) else str(value)
            self.producer.produce(
                topic=topic,
                key=key,
                value=message,
                callback=self._delivery_report
            )
            self.producer.flush()
            logger.info(f"🚀 Event sent to {topic}: {key}")
            return True
        except Exception as e:
            logger.error(f"💥 Failed to send event: {e}")
            return False
    
    def _delivery_report(self, err, msg):
        """Delivery callback - because we care about our messages"""
        if err is not None:
            logger.error(f"💥 Message delivery failed: {err}")
        else:
            logger.debug(f"✅ Message delivered to {msg.topic()} [{msg.partition()}]")

class KafkaConsumerBro:
    """The chillest Kafka consumer you'll ever meet"""
    
    def __init__(self, group_id: str, topics: list):
        self.config = {
            'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP", "localhost:9092"),
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(self.config)
        self.consumer.subscribe(topics)
    
    def consume_events(self, timeout: float = 1.0):
        """Consume events like a hungry code bro"""
        try:
            msg = self.consumer.poll(timeout)
            if msg is None:
                return None
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.info(f"End of partition reached {msg.topic()}")
                else:
                    logger.error(f"Consumer error: {msg.error()}")
                return None
            
            return {
                'topic': msg.topic(),
                'key': msg.key().decode('utf-8') if msg.key() else None,
                'value': json.loads(msg.value().decode('utf-8')),
                'partition': msg.partition(),
                'offset': msg.offset()
            }
        except Exception as e:
            logger.error(f"💥 Error consuming event: {e}")
            return None

def get_producer() -> KafkaProducerBro:
    """Get a producer instance - factory pattern, bro!"""
    return KafkaProducerBro()

def send_hr_event(event_type: str, data: Dict[str, Any], service_name: str = None):
    """Send HR-specific events with standardized format"""
    if not service_name:
        service_name = os.getenv('SERVICE_NAME', 'unknown')
    
    event_data = {
        'event_type': event_type,
        'service': service_name,
        'timestamp': '2025-08-03T14:48:32Z',
        'data': data
    }
    
    producer = get_producer()
    return producer.send_event('hr-events', f"{service_name}-{event_type}", event_data)

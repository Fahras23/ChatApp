from prometheus_client import Counter

# Define a counter for messages sent
messages_sent = Counter('messages_sent_total', 'Total number of messages sent')

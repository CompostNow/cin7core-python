# Barebones python wrapper for Cin7 Core API V2

Currently only supports Sale, Sale List, Sale Order, and Webhook endpoints.

## Usage

```python
from cin7core import Cin7Core

# Initialize client
c7c = Cin7Core(account_id=account_id, app_key=app_key)

# List all sales
c7c.sale.all().total
c7c.sale.all(page=3)

# Filter sales
c7c.sale.filter(UpdatedSince=updated_since)

# Get sale
c7c.sale.get(pk)

# Get only order details of sale
c7c.sale.order.get(pk)

# Update sale
c7c.sale.update(pk, data=data)

# Create webhook
c7c.webhook.create(data=webhook_data)

# Update webhook
c7c.webhook.update(pk, data=webhook_data)

# Remove webhook
c7c.webhook.delete(pk)
```
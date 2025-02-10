#!/bin/bash
echo "Testing API endpoints..."
curl -X GET http://127.0.0.1:8000/api/users/ -H "Content-Type: application/json"
curl -X GET http://127.0.0.1:8000/api/jobs/ -H "Content-Type: application/json"
curl -X GET http://127.0.0.1:8000/api/invoices/ -H "Content-Type: application/json"
curl -X GET http://127.0.0.1:8000/api/inventory/ -H "Content-Type: application/json"
curl -X GET http://127.0.0.1:8000/api/settings/ -H "Content-Type: application/json"
curl -X GET http://127.0.0.1:8000/api/synclogs/ -H "Content-Type: application/json"
echo "API test complete."

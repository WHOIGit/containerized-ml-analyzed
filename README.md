# Containerized "ml_analyzed"

Microservice for computing volume analyzed for IFCB data.

Example usage:

```
curl -X POST -F "adc_file=@/some/path/D20240203T123456_IFCB10.adc" http://localhost:8000/ml_analyzed
```

Returns a JSON structure, e.g.,

`{ "bin": "D20240203T123456_IFCB10", "ml_analyzed": 4.13948 }`

If the volume analyzed is nan, it will return null for the `ml_analyzed` key.

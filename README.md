# Number Classification API

## Description
A FastAPI-based service that analyzes numbers(integers) and returns their mathematical properties with interesting facts. This API performs various mathematical calculations including primality checks, perfect number verification, Armstrong number detection, and parity determination. It also integrates with the Numbers API to provide interesting mathematical facts about the given number.

## Features
- Mathematical property analysis (prime, perfect, armstrong numbers, parity)
- Digit sum calculation
- Integration with Numbers API for fun facts
- Request caching for improved performance
- CORS and Trusted Host middleware support
- Comprehensive error handling
- Environment-based configuration

## Local Setup

### Prerequisites
- Python 3.12 or higher

### Installation Steps
1. Clone the [repository](https://github.com/iamprecieee/stage-1-backend.git).

2. Create and activate a virtual environment:
    <details>
    <summary><b>macOS/Linux</b></summary>

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    </details>

    <details>
    <summary><b>Windows</b></summary>

    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
    </details>

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure environment variables:
    - Create a `.env` file in the project root
    - Modify these values as needed:
    ```env
    ALLOWED_ORIGINS=*
    ALLOWED_HOSTS=*
    USE_MIDDLEWARE=True
    NUMBERS_API_TIMEOUT=0
    NUMBERS_API_BASE_URL=http://numbersapi.com
    CACHE_EXPIRY=0
    CACHE_MAX_SIZE=0
    ```

5. Start the application:
    ```bash
    fastapi run app/main.py
    ```

## API Documentation

### Number Classification Endpoint

- **URL**: `/api/classify-number`
- **Method**: `GET`
- **Query Parameters**: 
  - `number` (required): Integer to analyze

#### Example Request
```bash
curl -X GET https://test.com/api/classify-number?number=371
```

#### Success Response (200 OK)
```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```

#### Error Response (400 Bad Request)
```json
{
    "number": "alphabet",
    "error": true
}
```

## Implementation Details

### Project Structure
```
app/
├── internal/
│   ├── cache.py          # Caching implementation
│   ├── config.py         # Settings
│   ├── dependencies.py   # FastAPI dependencies
│   ├── exceptions.py     # Custom exception
│   ├── middleware.py     # Middleware
│   ├── models.py         # Pydantic models
│   └── numbers.py        # Number analysis utilities
├── routers/
│   └── data.py           # API routes
└── main.py               # Application entry point
└── test_main.py          # Tests file
.env                      # Environmental variables
```

### Key Components

1. **Caching System**
   - In-memory caching with size limits and expiration
   - Cache eviction

2. **Number Analysis**
   - Efficient prime number checking
   - Efficient negative number handling
   - Perfect number verification
   - Armstrong number detection
   - Parity checking
   - Digit sum calculation

3. **External Integration**
   - Numbers API integration with retry logic
   - Timeout/Error handling

4. **Security**
   - CORS middleware
   - Trusted host verification
   - Input validation
   - Error handling

## Performance Considerations

This API implements several optimizations:
- Response caching with configurable expiration
- Asynchronous external API calls
- Request timeout configuration

## Testing

Run the test suite:
```bash
pytest -s
```
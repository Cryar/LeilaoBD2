from django.test import TestCase

# Create your tests here.

CALL inserir_user(
	1::INTEGER,
    'john_doe'::VARCHAR, 
	'12345'::VARCHAR,
	'john@example.com'::VARCHAR, 
    'John Doe'::VARCHAR, 
    'John'::VARCHAR, 
    1000.00::NUMERIC, 
    '123456789'::VARCHAR, 
    '123 Main St'::VARCHAR, 
    'New York'::VARCHAR,
	'12335'::VARCHAR,
	'portugal'::VARCHAR,
     current_date::date 
);
insert into toolshopgo.customers 
    (created_at, updated_at,deleted_at, name, vat_number, company_type, street_address, city, postal_code, country, contact_name, email, phone, industry, website, is_active)
SELECT NOW(), NOW(), NULL, customers_customer.name, customers_customer.vat_number, company_type, street_address, city, postal_code, country, contact_name, email, phone, industry, website, is_active 
    FROM toolshop.customers_customer;

insert into toolshopgo.invoices 
    (created_at, updated_at,deleted_at, invoice_number, due_date, total_amount, tax_amount, status)
SELECT NOW(), NOW(), NULL, invoice_number, due_date, total_amount, tax_amount, status
    FROM toolshop.invoices_invoice;

INSERT INTO toolshopgo.jobs 
    (created_at, updated_at, deleted_at, customer_id, job_title, description, status, start_date, end_date, cost_estimate, actual_cost)
SELECT NOW(), NOW(), NULL, customer_id, job_title, description, status, start_date, end_date, cost_estimate, actual_cost FROM toolshop.jobs_job;
-- Creating the employee table
CREATE TABLE employee (
    emp_id SERIAL PRIMARY KEY,    -- emp_id will be auto-incremented
    emp_name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,            -- Date of birth
    department_id INTEGER NOT NULL,
    emp_email VARCHAR(100) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE -- Boolean to indicate if the employee is active
);

-- Inserting records into the employee table
INSERT INTO employee (emp_name, dob, department_id, emp_email, is_active)
VALUES
    ('Alice Johnson', '1990-04-15', 1, 'alice.johnson@example.com', TRUE),
    ('Bob Smith', '1985-09-23', 2, 'bob.smith@example.com', TRUE),
    ('Charlie Brown', '1992-12-01', 3, 'charlie.brown@example.com', FALSE),
    ('Diana Ross', '1988-07-19', 2, 'diana.ross@example.com', TRUE),
    ('Evan Wright', '1995-11-30', 4, 'evan.wright@example.com', TRUE);

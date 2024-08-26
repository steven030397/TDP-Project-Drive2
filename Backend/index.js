const express = require('express');
const { Pool } = require('pg');

const app = express();
const port = 3000;

// PostgreSQL connection
const pool = new Pool({
  user: 'your_db_user',
  host: 'localhost',
  database: 'user_vehicle_db',
  password: 'your_db_password',
  port: 5432,
});

app.use(express.json()); // Middleware to parse JSON requests

// User Endpoints
app.get('/api/users', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM users');
    res.json(result.rows);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

app.post('/api/users', async (req, res) => {
  const { username, password, email } = req.body;
  try {
    const result = await pool.query(
      'INSERT INTO users (username, password, email) VALUES ($1, $2, $3) RETURNING *',
      [username, password, email]
    );
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// Vehicle Endpoints
app.get('/api/vehicles', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM vehicles');
    res.json(result.rows);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

app.post('/api/vehicles', async (req, res) => {
  const { user_id, car_model, license_plate, color } = req.body;
  try {
    const result = await pool.query(
      'INSERT INTO vehicles (user_id, car_model, license_plate, color) VALUES ($1, $2, $3, $4) RETURNING *',
      [user_id, car_model, license_plate, color]
    );
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// Travel Logs Endpoints
app.get('/api/travel-logs', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM travel_logs');
    res.json(result.rows);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

app.post('/api/travel-logs', async (req, res) => {
  const {
    user_id,
    start_latitude,
    start_longitude,
    start_point_name,
    end_latitude,
    end_longitude,
    end_point_name,
    start_time,
    end_time
  } = req.body;

  try {
    const result = await pool.query(
      `INSERT INTO travel_logs (
        user_id, start_latitude, start_longitude, start_point_name,
        end_latitude, end_longitude, end_point_name, start_time, end_time
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING *`,
      [
        user_id,
        start_latitude,
        start_longitude,
        start_point_name,
        end_latitude,
        end_longitude,
        end_point_name,
        start_time,
        end_time
      ]
    );
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// Matching Data Endpoints
app.get('/api/matching-data', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM matching_data');
    res.json(result.rows);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

app.post('/api/matching-data', async (req, res) => {
  const {
    user_id_person1,
    user_id_person2,
    match_time,
    start_point_name,
    end_point_name,
    status,
    driver_name
  } = req.body;

  try {
    const result = await pool.query(
      `INSERT INTO matching_data (
        user_id_person1, user_id_person2, match_time,
        start_point_name, end_point_name, status, driver_name
      ) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *`,
      [
        user_id_person1,
        user_id_person2,
        match_time,
        start_point_name,
        end_point_name,
        status,
        driver_name
      ]
    );
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});

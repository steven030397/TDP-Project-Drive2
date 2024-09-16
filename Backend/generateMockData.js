npm install @faker-js/faker
npm install pg

const { Pool } = require('pg');
const { faker } = require('@faker-js/faker');

// PostgreSQL connection
const pool = new Pool({
  connectionString: 'postgres://your-username:your-password@hostname:port/your-database-name',
  ssl: {
    rejectUnauthorized: false,
  }
});

// Function to insert mock data
async function generateMockData() {
  try {
    // Generate 100 users
    for (let i = 0; i < 100; i++) {
      const username = faker.internet.userName();
      const password = faker.internet.password();
      const email = faker.internet.email();

      await pool.query(
        'INSERT INTO users (username, password, email) VALUES ($1, $2, $3)',
        [username, password, email]
      );
    }

    // Generate 100 car models
    for (let i = 0; i < 100; i++) {
      const model_name = faker.vehicle.model();
      const manufacturer = faker.vehicle.manufacturer();
      const year_of_manufacture = faker.date.past(30).getFullYear();

      await pool.query(
        'INSERT INTO car_models (model_name, manufacturer, year_of_manufacture) VALUES ($1, $2, $3)',
        [model_name, manufacturer, year_of_manufacture]
      );
    }

    // Generate 100 vehicles
    for (let i = 0; i < 100; i++) {
      const user_id = Math.floor(Math.random() * 100) + 1;
      const car_model = faker.vehicle.model();
      const license_plate = faker.vehicle.vrm();
      const color = faker.vehicle.color();

      await pool.query(
        'INSERT INTO vehicles (user_id, car_model, license_plate, color) VALUES ($1, $2, $3, $4)',
        [user_id, car_model, license_plate, color]
      );
    }

    // Generate 100 travel logs
    for (let i = 0; i < 100; i++) {
      const user_id = Math.floor(Math.random() * 100) + 1;
      const start_latitude = parseFloat(faker.address.latitude());
      const start_longitude = parseFloat(faker.address.longitude());
      const start_point_name = faker.address.streetAddress();
      const end_latitude = parseFloat(faker.address.latitude());
      const end_longitude = parseFloat(faker.address.longitude());
      const end_point_name = faker.address.streetAddress();
      const start_time = faker.date.past();
      const end_time = faker.date.soon(1, start_time);

      await pool.query(
        `INSERT INTO travel_logs (
          user_id, start_latitude, start_longitude, start_point_name,
          end_latitude, end_longitude, end_point_name, start_time, end_time
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
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
    }

    // Generate 100 matching data entries
    for (let i = 0; i < 100; i++) {
      const user_id_person1 = Math.floor(Math.random() * 100) + 1;
      const user_id_person2 = Math.floor(Math.random() * 100) + 1;
      const match_time = faker.date.past();
      const start_point_name = faker.address.streetAddress();
      const end_point_name = faker.address.streetAddress();
      const status = faker.random.arrayElement(['active', 'completed']);
      //const driver_name = faker.name.findName();

      await pool.query(
        `INSERT INTO matching_data (
          user_id_person1, user_id_person2, match_time, start_point_name, 
          end_point_name, status, driver_name
        ) VALUES ($1, $2, $3, $4, $5, $6, $7)`,
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
    }

    console.log('Mock data generation completed.');
  } catch (err) {
    console.error('Error generating mock data:', err.message);
  } finally {
    pool.end();
  }
}

// Run the function to generate mock data
generateMockData();

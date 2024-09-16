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
    // Generate 150 users
    for (let i = 0; i < 150; i++) {
      const username = faker.internet.userName();
      const password = faker.internet.password();
      const email = faker.internet.email();

      await pool.query(
        'INSERT INTO users (username, password, email) VALUES ($1, $2, $3)',
        [username, password, email]
      );
    }

    // Generate 150 user personal details
    for (let i = 0; i < 150; i++) {
      const first_name = faker.name.firstName();
      const middle_name = faker.name.middleName();
      const last_name = faker.name.lastName();
      const date_of_birth = faker.date.past(30, new Date(2000, 0, 1));
      const gender = faker.helpers.arrayElement(['Male', 'Female', 'Other']);
      const phone_number = faker.phone.number();
      const address = faker.address.streetAddress();
      const state = faker.address.state();
      const driver_license_number = faker.random.alphaNumeric(10);
      const has_car = faker.datatype.boolean();

      await pool.query(
        `INSERT INTO user_personal_details (
          first_name, middle_name, last_name, date_of_birth, gender, 
          phone_number, address, state, driver_license_number, has_car
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)`,
        [
          first_name,
          middle_name,
          last_name,
          date_of_birth,
          gender,
          phone_number,
          address,
          state,
          driver_license_number,
          has_car
        ]
      );
    }

    // Generate 150 vehicles
    for (let i = 0; i < 150; i++) {
      const user_id = Math.floor(Math.random() * 150) + 1;
      const car_model = faker.vehicle.model();
      const license_plate = faker.vehicle.vrm();
      const color = faker.vehicle.color();

      await pool.query(
        'INSERT INTO vehicles (user_id, car_model, license_plate, color) VALUES ($1, $2, $3, $4)',
        [user_id, car_model, license_plate, color]
      );
    }

    // Generate 150 car models
    for (let i = 0; i < 150; i++) {
      const model_name = faker.vehicle.model();
      const manufacturer = faker.vehicle.manufacturer();
      const year_of_manufacture = faker.date.past(30).getFullYear();

      await pool.query(
        'INSERT INTO car_models (model_name, manufacturer, year_of_manufacture) VALUES ($1, $2, $3)',
        [model_name, manufacturer, year_of_manufacture]
      );
    }

    // Generate 150 travel logs
    for (let i = 0; i < 150; i++) {
      const user_id = Math.floor(Math.random() * 150) + 1;
      const start_latitude = parseFloat(faker.address.latitude());
      const start_longitude = parseFloat(faker.address.longitude());
      const start_point_name = faker.address.streetAddress();
      const end_latitude = parseFloat(faker.address.latitude());
      const end_longitude = parseFloat(faker.address.longitude());
      const end_point_name = faker.address.streetAddress();
      const start_time = faker.date.past();
      const end_time = faker.date.soon(1, start_time);
      const travel_days = `{${faker.helpers.arrayElements(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).join(',')}}`;
      const weekly_mileage_percentage = faker.datatype.float({ min: 0, max: 100, precision: 0.01 });
      const weekly_fuel_spent = faker.commerce.price(50, 200, 2);

      await pool.query(
        `INSERT INTO travel_logs (
          user_id, start_latitude, start_longitude, start_point_name,
          end_latitude, end_longitude, end_point_name, start_time, end_time,
          travel_days, weekly_mileage_percentage, weekly_fuel_spent
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)`,
        [
          user_id,
          start_latitude,
          start_longitude,
          start_point_name,
          end_latitude,
          end_longitude,
          end_point_name,
          start_time,
          end_time,
          travel_days,
          weekly_mileage_percentage,
          weekly_fuel_spent
        ]
      );
    }

    // Generate 150 matching data entries
    for (let i = 0; i < 150; i++) {
      const user_id_person1 = Math.floor(Math.random() * 150) + 1;
      const user_id_person2 = Math.floor(Math.random() * 150) + 1;
      const match_time = faker.date.past();
      const start_point_name = faker.address.streetAddress();
      const end_point_name = faker.address.streetAddress();
      const status = faker.helpers.arrayElement(['active', 'completed']);
      const driver_name = faker.name.findName();

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
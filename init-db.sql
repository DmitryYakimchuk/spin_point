CREATE DATABASE spin_point_db;
CREATE USER spin_point WITH PASSWORD '111';
GRANT ALL PRIVILEGES ON DATABASE spin_point_db TO spin_point;

\c spin_point_db;

GRANT ALL PRIVILEGES ON SCHEMA public TO spin_point;
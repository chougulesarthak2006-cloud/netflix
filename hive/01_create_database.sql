-- ==============================================================================
-- Script: 01_create_database.sql
-- Project: Netflix Movies and TV Shows Data Analysis using Hadoop and Hive
-- Purpose: Create and configure the project database in Apache Hive.
-- ==============================================================================

-- 1. Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS netflix_db
COMMENT 'Database for Netflix Movies and TV Shows Data Analysis Project'
WITH DBPROPERTIES ('creator' = 'Hadoop Student', 'created_for' = 'Big Data Micro-Project');

-- 2. Verify database creation
SHOW DATABASES;

-- 3. Inspect database metadata and HDFS storage location
DESCRIBE DATABASE EXTENDED netflix_db;

-- 4. Set the current database context to netflix_db
USE netflix_db;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS project_category;
DROP TABLE IF EXISTS activity_importances;
DROP TABLE IF EXISTS stages;
DROP TABLE IF EXISTS milestones;


CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    project_title TEXT UNIQUE NOT NULL,
    project_description TEXT NOT NULL,
    completion_rate INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP DEFAULT NULL,
    FOREIGN KEY (author_id) REFERENCES users (user_id)
);

CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_code TEXT UNIQUE NOT NULL,
    category_description TEXT NOT NULL
);

CREATE TABLE project_category (
    category_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    PRIMARY KEY (category_id, project_id),
    FOREIGN KEY (category_id) REFERENCES categories (category_id),
    FOREIGN KEY (project_id) REFERENCES projects (project_id)
);

CREATE TABLE activity_importances (
    activity_importance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_code TEXT UNIQUE NOT NULL,
    activity_description TEXT UNIQUE NOT NULL
);

CREATE TABLE stages (
    stage_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stage_code TEXT UNIQUE NOT NULL,
    stage_description TEXT NOT NULL
);

CREATE TABLE milestones (
    milestone_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    activity_importance_id INTEGER NOT NULL,
    stage_id INTEGER NOT NULL,
    milestone_title TEXT NOT NULL,
    milestone_description TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP DEFAULT NULL,
    milestone_observation TEXT DEFAULT NULL,
    FOREIGN KEY (project_id) REFERENCES projects (project_id),
    FOREIGN KEY (activity_importance_id) REFERENCES activity_importances (activity_importance_id),
    FOREIGN KEY (stage_id) REFERENCES stages (stage_id)
);




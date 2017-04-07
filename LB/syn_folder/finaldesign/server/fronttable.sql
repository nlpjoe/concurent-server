CREATE TABLE TypeTable(
id int auto_increment primary key,
name varchar(32)
);

CREATE TABLE FrontDataTable(
IP          varchar(32) not null,
typeid      int         references TypeTable(id),
datetime    varchar(32) not null,
data        varchar(32)
);

INSERT INTO TypeTable (name) VALUES ('PM2.5');          -- 悬浮颗粒 µg/m³ 微米 (颗粒直径小于10则可吸入，小于2.5则十分有害)
INSERT INTO TypeTable (name) VALUES ('Humidity');       -- 克/立方米(每立方米有多少克水)
INSERT INTO TypeTable (name) VALUES ('Temperature');    -- 摄氏度
INSERT INTO TypeTable (name) VALUES ('VehicleSpeed');            -- 车速 km/h

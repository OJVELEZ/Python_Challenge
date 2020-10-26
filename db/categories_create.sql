CREATE TABLE IF NOT EXISTS main_category(
    main_id integer primary key autoincrement,
    count integer,
    uptime text,
    cversion integer,
    rpriceallowed integer,
    minpriceallowed text,
    xmltimestamp  text,
    xmlack  text,
    xmlversion integer,
    xmlbuild text
);

CREATE TABLE IF NOT EXISTS categories(
    categories_id integer primary key autoincrement,
    categoryid integer,
    bestoffer integer,
    autopay integer,
    categorylevel integer,
    categoryname text,
    categoryparent integer,
    FOREIGN KEY (main_id) REFERENCES main_category(main_id)
);
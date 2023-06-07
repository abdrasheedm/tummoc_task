select r1.route_id,
    r1.stop_id AS source_stop_id,
    r2.stop_id AS dest_stop_id
FROM route_points AS r1
    JOIN route_points AS r2 ON r1.route_id = r2.route_id
WHERE r1.order < r2.order
    AND r1.route_id = r1.order
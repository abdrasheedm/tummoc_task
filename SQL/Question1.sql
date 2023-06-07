

select rp.route_id, r.name, SUM(rp.distance) AS total_distance
FROM 
routes AS r
JOIN
route_points AS rp ON r.id = rp.route_id
GROUP BY
rp.route_id, r.name;

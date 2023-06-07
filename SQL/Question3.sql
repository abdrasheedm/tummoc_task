SELECT
  s.id AS station_id,
  s.name AS station_name,
  t.slot,
  t.time
FROM
  station AS s
  JOIN times AS t ON s.id = t.station_id
WHERE
  s.id = 1           
  AND t.slot = 1;
  
USE SAKILA ;

SELECT 
DATE(r.rental_date) as rental_day,
i.store_id,
sum(p.amount) as revenue
from rental r 
JOIN inventory i 
ON i.inventory_id = r.inventory_id
JOIN payment p
ON p.rental_id = r.rental_id
WHERE r.rental_date < '2006-01-01'
group by rental_day, i.store_id
ORDER BY rental_day;

SELECT 
i.store_id,
sum(p.amount) as revenue
from rental r 
JOIN inventory i 
ON i.inventory_id = r.inventory_id
JOIN payment p
ON p.rental_id = r.rental_id
WHERE r.rental_date < '2006-01-01'
group by i.store_id
ORDER BY i.store_id;

SELECT 
f.title,
count(r.rental_id) as num_of_rents,
i.store_id
FROM
rental r 
JOIN inventory i USING (inventory_id)
JOIN film f USING (film_id)
where r.rental_date < '2006-01-01'
group by i.store_id, i.film_id
order by num_of_rents DESC;



WITH ranked AS (
    SELECT 
        i.store_id,
        f.title,
        COUNT(r.rental_id) AS rental_count,
        ROW_NUMBER() OVER (
            PARTITION BY i.store_id
            ORDER BY COUNT(r.rental_id) DESC
        ) AS rn
    FROM rental r
    JOIN inventory i USING (inventory_id)
    JOIN film f USING (film_id)
    WHERE EXTRACT(YEAR FROM r.rental_date) = 2005
    GROUP BY i.store_id, f.title
)
SELECT store_id, title, rental_count
FROM ranked
WHERE rn <= 5
ORDER BY store_id, rn;



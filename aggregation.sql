DROP TABLE IF EXISTS datesByMonth;
DROP TABLE IF EXISTS catSoldVolByMonth;
DROP TABLE IF EXISTS catSoldRevByMonth;


--Group dates into months and rank by recency
SELECT dateid, caldate, year, EXTRACT(month FROM caldate) as month,
  dense_rank() OVER (ORDER BY year DESC, EXTRACT(month FROM caldate) DESC) AS month_rank
INTO datesByMonth
FROM date;



--  total sales by revenue

SELECT  m.month_rank,  m.year, m.month, c.catid, c.catname, sum(s.qtysold*s.pricepaid) as totalsalesRev
INTO catSoldRevByMonth
FROM category c, event e, sales s, datesByMonth m
WHERE
c.catid=e.catid AND
s.eventid=e.eventid AND
s.dateid=m.dateid
GROUP BY c.catid, c.catname, m.month_rank, m.year, m.month;


--limit to top 3 categories for each month

with revRankedByMonth as
(select month_rank,  year, month, catid, catname, totalsalesRev,
rank() over (partition by month_rank order by totalsalesrev desc) as rnk
from catSoldRevByMonth )
select * from revRankedByMonth where rnk<4
order by month_rank, totalsalesRev desc;




--total sales by ticket volume


SELECT  m.month_rank,  m.year, m.month, c.catid, c.catname, sum(s.qtysold) as totalsalesQty
INTO catSoldVolByMonth
FROM category c, event e, sales s, datesByMonth m
WHERE
c.catid=e.catid AND
s.eventid=e.eventid AND
s.dateid=m.dateid
GROUP BY c.catid, c.catname, m.month_rank, m.year, m.month;

--limit to top 3 categories for each month

with volRankedByMonth as
(select month_rank,  year, month, catid, catname, totalsalesQty,
rank() over (partition by month_rank order by totalsalesQty desc) as rnk
from catSoldVolByMonth )
select * from volRankedByMonth where rnk<4
order by month_rank, totalsalesQty desc;

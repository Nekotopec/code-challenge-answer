select e1.department, e2.name, e1.max
from (
select department, max(salary) as max
    from employee
    group by department
) as e1 join employee as e2 on e2.salary=e1.max;
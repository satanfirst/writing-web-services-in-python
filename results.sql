use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product

-- 2. Выбрать названия всех автоматизированных складов
select name from store where is_automated = 1

-- 3. Посчитать общую сумму в деньгах всех продаж
select sum(total) from sale

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
select distinct store_id from sale


-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
select distinct s.store_id from store s left join sale ON s.store_id = sale.store_id where sale.store_id is null


-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
select any_value(p.name), avg(s.total/s.quantity) from sale s left outer join product p on p.product_id = s.product_id group by p.name

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select any_value(p.name) from product p natural join sale s group by p.product_id having count(distinct s.store_id) = 1

-- 8. Получить названия всех складов, с которых продавался только один продукт
select any_value(s.name) from store s natural join sale ss group by ss.product_id having count(DISTINCT s.store_id)=1

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * from sale where total = (select max(total) from sale)

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select date from sale group by date order by sum(total) DESC, date ASC limit 1


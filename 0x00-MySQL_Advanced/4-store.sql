-- SQL script that creates trigger
-- SQL command
CREATE TRIGGER decr_qty AFTER INSERT ON orders
  FOR EACH ROW
    UPDATE items SET quantity = quantity - NEW.number
      WHERE name = NEW.item_name;

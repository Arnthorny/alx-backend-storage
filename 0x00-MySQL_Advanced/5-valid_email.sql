-- SQL script that creates trigger
-- SQL command
DELIMITER $$
CREATE TRIGGER email_reset BEFORE UPDATE ON users
  FOR EACH ROW
   BEGIN
    IF STRCMP(OLD.email, NEW.email) THEN
      SET NEW.valid_email = NOT OLD.valid_email;
    END IF;
  END$$
DELIMITER ;

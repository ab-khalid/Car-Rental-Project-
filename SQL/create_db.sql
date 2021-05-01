-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema car_rental
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema car_rental
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `car_rental` DEFAULT CHARACTER SET utf8 ;
USE `car_rental` ;

-- -----------------------------------------------------
-- Table `car_rental`.`Admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `car_rental`.`Admin` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NULL,
  `hashed_password` TEXT(128) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `car_rental`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `car_rental`.`User` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NULL,
  `hashed_password` TEXT(128) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `car_rental`.`Car`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `car_rental`.`Car` (
  `VIN` VARCHAR(45) NOT NULL,
  `Make` VARCHAR(45) NULL,
  `Model` VARCHAR(45) NULL,
  `Color` VARCHAR(45) NULL,
  `Year` INT NULL,
  `Price` DECIMAL(10,2) NULL,
  PRIMARY KEY (`VIN`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `car_rental`.`Saved_List`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `car_rental`.`Saved_List` (
  `User_id` INT NOT NULL,
  `Car_VIN` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`User_id`, `Car_VIN`),
  CONSTRAINT `fk_Car_has_User_Car`
    FOREIGN KEY (`Car_VIN`)
    REFERENCES `car_rental`.`Car` (`VIN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Car_has_User_User1`
    FOREIGN KEY (`User_id`)
    REFERENCES `car_rental`.`User` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `car_rental`.`Rental`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `car_rental`.`Rental` (
  `Order_Number` INT NOT NULL AUTO_INCREMENT,
  `User_id` INT NOT NULL,
  `Car_VIN` VARCHAR(45) NOT NULL,
  `Date` DATETIME(3) NOT NULL,
  `Rental_Days` INT NOT NULL,
  `Price` DECIMAL(10,2) NOT NULL,
  `Return Date` DATETIME(3) NOT NULL,
  PRIMARY KEY (`Order_Number`),
  CONSTRAINT `fk_Car_has_User_Car1`
    FOREIGN KEY (`Car_VIN`)
    REFERENCES `car_rental`.`Car` (`VIN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Car_has_User_User2`
    FOREIGN KEY (`User_id`)
    REFERENCES `car_rental`.`User` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `car_rental`.`Image`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `car_rental`.`Image` (
  `image_Number` INT NOT NULL,
  `Car_VIN` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`image_Number`),
  CONSTRAINT `fk_Image_Car1`
    FOREIGN KEY (`Car_VIN`)
    REFERENCES `car_rental`.`Car` (`VIN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

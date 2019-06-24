ALTER TABLE `orders`
ADD COLUMN `item_count` INT NULL AFTER `invoice_amount`;

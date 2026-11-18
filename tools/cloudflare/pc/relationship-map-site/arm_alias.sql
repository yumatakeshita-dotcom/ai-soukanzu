CREATE TABLE IF NOT EXISTS company_alias (slug TEXT, alias TEXT);
CREATE INDEX IF NOT EXISTS i_calias ON company_alias(alias);
DELETE FROM company_alias WHERE slug='arm_holdings';
INSERT INTO company_alias VALUES ('arm_holdings','Arm');
INSERT INTO company_alias VALUES ('arm_holdings','ARM');
INSERT INTO company_alias VALUES ('arm_holdings','アーム');
INSERT INTO company_alias VALUES ('arm_holdings','アームホールディングス');
INSERT INTO company_alias VALUES ('arm_holdings','ARMホールディングス');
INSERT INTO company_alias VALUES ('arm_holdings','Arm Ltd');

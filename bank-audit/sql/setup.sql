-- ============================================
-- BASE DE DONNÉES: bank_audit
-- ============================================
CREATE DATABASE IF NOT EXISTS bank_audit CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bank_audit;

-- ============================================
-- TABLE CLIENT
-- ============================================
CREATE TABLE IF NOT EXISTS client (
    n_compte VARCHAR(20) PRIMARY KEY,
    nomclient VARCHAR(100) NOT NULL,
    solde DECIMAL(15,2) DEFAULT 0.00
);

-- ============================================
-- TABLE RETRAIT
-- ============================================
CREATE TABLE IF NOT EXISTS retrait (
    n_retrait INT AUTO_INCREMENT PRIMARY KEY,
    n_cheque VARCHAR(30) NOT NULL,
    n_compte VARCHAR(20) NOT NULL,
    montant DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (n_compte) REFERENCES client(n_compte)
);

-- ============================================
-- TABLE AUDIT_RETRAIT
-- ============================================
CREATE TABLE IF NOT EXISTS audit_retrait (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type_action ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    date_maj DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    n_retrait INT,
    n_compte VARCHAR(20),
    nomclient VARCHAR(100),
    montant_ancien DECIMAL(15,2),
    montant_nouv DECIMAL(15,2),
    utilisateur VARCHAR(100)
);

-- ============================================
-- TRIGGER: AFTER INSERT sur retrait
-- ============================================
DELIMITER $$
CREATE TRIGGER trg_retrait_insert
AFTER INSERT ON retrait
FOR EACH ROW
BEGIN
    DECLARE v_nomclient VARCHAR(100);
    SELECT nomclient INTO v_nomclient FROM client WHERE n_compte = NEW.n_compte;
    
    INSERT INTO audit_retrait (type_action, date_maj, n_retrait, n_compte, nomclient, montant_ancien, montant_nouv, utilisateur)
    VALUES ('INSERT', NOW(), NEW.n_retrait, NEW.n_compte, v_nomclient, 0, NEW.montant, CURRENT_USER());
    
    -- Mettre à jour le solde du client
    UPDATE client SET solde = solde - NEW.montant WHERE n_compte = NEW.n_compte;
END$$

-- ============================================
-- TRIGGER: AFTER UPDATE sur retrait
-- ============================================
CREATE TRIGGER trg_retrait_update
AFTER UPDATE ON retrait
FOR EACH ROW
BEGIN
    DECLARE v_nomclient VARCHAR(100);
    SELECT nomclient INTO v_nomclient FROM client WHERE n_compte = NEW.n_compte;
    
    INSERT INTO audit_retrait (type_action, date_maj, n_retrait, n_compte, nomclient, montant_ancien, montant_nouv, utilisateur)
    VALUES ('UPDATE', NOW(), NEW.n_retrait, NEW.n_compte, v_nomclient, OLD.montant, NEW.montant, CURRENT_USER());
    
    -- Recalculer le solde: solde = solde + ancien_montant - nouveau_montant
    UPDATE client 
    SET solde = solde + OLD.montant - NEW.montant 
    WHERE n_compte = NEW.n_compte;
END$$

-- ============================================
-- TRIGGER: AFTER DELETE sur retrait
-- ============================================
CREATE TRIGGER trg_retrait_delete
AFTER DELETE ON retrait
FOR EACH ROW
BEGIN
    DECLARE v_nomclient VARCHAR(100);
    SELECT nomclient INTO v_nomclient FROM client WHERE n_compte = OLD.n_compte;
    
    INSERT INTO audit_retrait (type_action, date_maj, n_retrait, n_compte, nomclient, montant_ancien, montant_nouv, utilisateur)
    VALUES ('DELETE', NOW(), OLD.n_retrait, OLD.n_compte, v_nomclient, OLD.montant, 0, CURRENT_USER());
    
    -- Rembourser le solde
    UPDATE client SET solde = solde + OLD.montant WHERE n_compte = OLD.n_compte;
END$$
DELIMITER ;

-- ============================================
-- DONNÉES DE TEST
-- ============================================
INSERT INTO client (n_compte, nomclient, solde) VALUES
('ACC001', 'Jean Dupont', 5000.00),
('ACC002', 'Marie Martin', 8500.00),
('ACC003', 'Pierre Bernard', 12000.00);

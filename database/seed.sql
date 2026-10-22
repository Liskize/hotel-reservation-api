INSERT INTO hotels (nom, ville, adresse, nombre_chambres, created_at)
SELECT seed.nom, seed.ville, seed.adresse, seed.nombre_chambres, CURRENT_TIMESTAMP
FROM (
    VALUES
        ('Hotel Faso Lumiere', 'Ouagadougou', 'Avenue Kwame Nkrumah', 50),
        ('Residence Ouaga 2000', 'Ouagadougou', 'Quartier Ouaga 2000', 30)
) AS seed (nom, ville, adresse, nombre_chambres)
WHERE NOT EXISTS (
    SELECT 1
    FROM hotels AS existing
    WHERE existing.nom = seed.nom
      AND existing.ville = seed.ville
);

INSERT INTO clients (nom, prenom, email, telephone, created_at)
VALUES
    ('SANON', 'Cheick Hadou', 'cheickisanon@gmail.com', '+22675000000', CURRENT_TIMESTAMP),
    ('OUEDRAOGO', 'Judicaël', 'judicael.ouedraogo@example.com', '+22670000000', CURRENT_TIMESTAMP)
ON CONFLICT (email) DO UPDATE SET
    nom = EXCLUDED.nom,
    prenom = EXCLUDED.prenom,
    telephone = EXCLUDED.telephone;

INSERT INTO reservations (
    hotel_id,
    client_id,
    date_debut,
    date_fin,
    statut,
    montant_total,
    created_at
)
SELECT
    h.id,
    c.id,
    DATE '2026-11-10',
    DATE '2026-11-15',
    'CONFIRMEE',
    185000.00,
    CURRENT_TIMESTAMP
FROM hotels AS h
JOIN clients AS c ON c.email = 'cheickisanon@gmail.com'
WHERE h.nom = 'Hotel Faso Lumiere'
ON CONFLICT (hotel_id, client_id, date_debut, date_fin) DO NOTHING;

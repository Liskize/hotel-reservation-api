INSERT INTO hotels (nom, ville, adresse, nombre_chambres)
VALUES
    ('Hotel Central', 'Libreville', 'Boulevard de l''Independance', 50),
    ('Residence Ocean', 'Port-Gentil', 'Avenue du Bord de Mer', 30)
ON CONFLICT DO NOTHING;

INSERT INTO clients (nom, prenom, email, telephone)
VALUES
    ('Mba', 'Alice', 'alice.mba@example.com', '+241060000001'),
    ('Nze', 'Paul', 'paul.nze@example.com', '+241060000002')
ON CONFLICT (email) DO NOTHING;

INSERT INTO reservations (
    hotel_id,
    client_id,
    date_debut,
    date_fin,
    statut,
    montant_total
)
SELECT h.id, c.id, DATE '2026-11-10', DATE '2026-11-15', 'CONFIRMEE', 250000.00
FROM hotels AS h
JOIN clients AS c ON c.email = 'alice.mba@example.com'
WHERE h.nom = 'Hotel Central'
ON CONFLICT (hotel_id, client_id, date_debut, date_fin) DO NOTHING;

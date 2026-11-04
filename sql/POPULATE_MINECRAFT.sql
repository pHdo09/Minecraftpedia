INSERT INTO EFEITO (Nome, Nível, Tempo_de_Efeito, Tipo_de_efeito) VALUES
('Velocidade', 1, 200, 'Positivo'), ('Lentidão', 2, 200, 'Negativo'), ('Força', 3, 300, 'Positivo'),
('Fraqueza', 4, 300, 'Negativo'), ('Regeneração', 5, 150, 'Positivo'), ('Veneno', 6, 100, 'Negativo'),
('Fome', 7, 250, 'Negativo'), ('Saturação', 8, 50, 'Positivo'), ('Invisibilidade', 9, 400, 'Positivo'),
('Resistência', 10, 350, 'Positivo');

INSERT INTO INVENTÁRIO (id_inventário, Número_de_Slots, Classe_Inventário) VALUES
(1, 36, 'Jogador'), (2, 36, 'Jogador'), (3, 36, 'Jogador'), (4, 36, 'Jogador'), (5, 36, 'Jogador'),
(6, 36, 'Jogador'), (7, 36, 'Jogador'), (8, 36, 'Jogador'), (9, 36, 'Jogador'), (10, 36, 'Jogador'),
(11, 27, 'Baú'), (12, 54, 'Baú Grande'), (13, 27, 'Baú'), (14, 54, 'Baú Grande'), (15, 27, 'Baú');

INSERT INTO JOGADOR (Nickname, Vida, Dano_Base, Fome, Experiência, Fôlego, Armadura, Hitbox, Velocidade, Pulo, Inventário, Efeito, Nível) VALUES
('Steve01', 20, 4, 20, 0, 300, 0, 2, 100, 1, 1, 'Velocidade', 1),
('Alex02', 20, 4, 18, 150, 300, 4, 2, 100, 1, 2, 'Lentidão', 2),
('Notch03', 20, 5, 20, 9999, 300, 20, 2, 120, 1, 3, 'Força', 3),
('Herobrine04', 20, 6, 15, 500, 250, 10, 2, 90, 1, 4, 'Fraqueza', 4),
('Miner05', 20, 3, 12, 80, 300, 6, 2, 100, 1, 5, 'Regeneração', 5),
('Builder06', 18, 3, 20, 40, 300, 2, 2, 100, 1, 6, 'Veneno', 6),
('Explorer07', 20, 4, 10, 220, 280, 8, 2, 110, 1, 7, 'Fome', 7),
('Warrior08', 20, 8, 20, 600, 300, 18, 2, 95, 1, 8, 'Saturação', 8),
('Farmer09', 20, 2, 20, 30, 300, 0, 2, 100, 1, 9, 'Invisibilidade', 9),
('Enchanter10', 20, 4, 17, 999, 300, 12, 2, 100, 1, 10, 'Resistência', 10);

INSERT INTO TIPO_MOB (Nome, Vida, Dano_Base, Fôlego, Hitbox, Velocidade, Pulo, XP_Dropável, Raio_de_detecção, Prociável, Armadura, Item_Carregável, Classe_Mob) VALUES
('Zumbi', 20, 3, 300, 2, 95, 1, 5, 16, true, 2, 1, 'Hostil'),
('Esqueleto', 20, 4, 300, 2, 100, 1, 5, 16, true, 0, 1, 'Hostil'),
('Creeper', 20, 0, 300, 2, 90, 1, 5, 16, false, 0, 0, 'Hostil'),
('Aranha', 16, 2, 300, 2, 110, 2, 5, 16, true, 0, 0, 'Hostil'),
('Bruxa', 26, 3, 300, 2, 100, 1, 5, 16, true, 0, 1, 'Hostil'),
('Vaca', 10, 0, 300, 2, 90, 1, 3, 10, false, 0, 0, 'Pacífico'),
('Porco', 10, 0, 300, 2, 90, 1, 3, 10, false, 0, 0, 'Pacífico'),
('Ovelha', 8, 0, 300, 2, 90, 1, 3, 10, false, 0, 0, 'Pacífico'),
('Cavalo', 15, 0, 300, 2, 140, 2, 3, 10, false, 0, 0, 'Pacífico'),
('Gato', 10, 2, 300, 1, 120, 1, 3, 10, false, 0, 0, 'Pacífico'),
('Enderman', 40, 7, 300, 3, 100, 3, 5, 64, true, 0, 1, 'Neutro'),
('Lobo', 8, 4, 300, 2, 110, 2, 3, 16, false, 0, 0, 'Neutro'),
('Piglin', 20, 5, 300, 2, 100, 1, 5, 16, true, 4, 1, 'Neutro'),
('Abelha', 10, 2, 300, 1, 90, 1, 3, 8, false, 0, 0, 'Neutro'),
('Panda', 20, 0, 300, 2, 80, 1, 5, 10, false, 0, 0, 'Neutro');

INSERT INTO MUNDO (Save, Seed, Nome, Dificuldade, Permitir_comandos, Tipo, Modo, Gerar_baú_bônus, Gerar_estruturas, Experimentos, Pacote_de_Dados, Jogador) VALUES
('save_steve01', 123456, 'Mundo de Steve', 'Normal', true, 'Padrão', 'Sobrevivência', false, true, false, 'Vanilla', 'Steve01'),
('save_alex02', 234567, 'Reino de Alex', 'Difícil', false, 'Grande Bioma', 'Sobrevivência', true, true, false, 'Vanilla', 'Alex02'),
('save_notch03', 345678, 'Terra de Notch', 'Fácil', true, 'Padrão', 'Criativo', false, true, true, 'Vanilla', 'Notch03'),
('save_herobrine04', 456789, 'Sombra de Herobrine', 'Difícil', false, 'Amplificado', 'Sobrevivência', false, true, false, 'Vanilla', 'Herobrine04'),
('save_miner05', 567890, 'Mina do Miner', 'Normal', false, 'Padrão', 'Sobrevivência', false, false, false, 'Vanilla', 'Miner05'),
('save_builder06', 678901, 'Cidade do Builder', 'Pacífico', true, 'Padrão', 'Criativo', false, true, false, 'Vanilla', 'Builder06'),
('save_explorer07', 789012, 'Expedição Explorer', 'Normal', false, 'Padrão', 'Sobrevivência', true, true, false, 'Vanilla', 'Explorer07'),
('save_warrior08', 890123, 'Arena do Warrior', 'Difícil', true, 'Padrão', 'Sobrevivência Hardcore', false, true, false, 'Vanilla', 'Warrior08'),
('save_farmer09', 901234, 'Fazenda do Farmer', 'Fácil', false, 'Padrão', 'Sobrevivência', false, false, false, 'Vanilla', 'Farmer09'),
('save_enchanter10', 112233, 'Torre do Enchanter', 'Normal', false, 'Padrão', 'Sobrevivência', false, true, true, 'Vanilla', 'Enchanter10');

INSERT INTO DIMENSÃO (Nome, Aparência_Visual, Pode_dormir, Mundo) VALUES
('OW_Steve', 'Verde e Azul', true, 'save_steve01'), ('OW_Alex', 'Deserto e Selva', true, 'save_alex02'),
('OW_Notch', 'Planície Infinita', true, 'save_notch03'), ('OW_Herobrine', 'Sombrio', false, 'save_herobrine04'),
('OW_Miner', 'Montanhoso', true, 'save_miner05'), ('OW_Builder', 'Urbano', true, 'save_builder06'),
('OW_Explorer', 'Selvagem', true, 'save_explorer07'), ('OW_Warrior', 'Árido', true, 'save_warrior08'),
('OW_Farmer', 'Fértil', true, 'save_farmer09'), ('OW_Enchanter', 'Místico', true, 'save_enchanter10');

INSERT INTO TIPO_BIOMA (Nome, Altitude_Média, Temperatura, Tipo_de_Precipitação, Cor_da_Folhagem, Cor_da_água, Dimensão) VALUES
('Floresta', 70, 15, 'Chuva', 'Verde', 'Azul', 'OW_Steve'), ('Deserto', 65, 35, 'Nenhuma', 'Amarelo', 'Turquesa', 'OW_Alex'),
('Planície', 68, 20, 'Chuva', 'Verde Claro', 'Azul', 'OW_Notch'), ('Caverna Escura', 20, 10, 'Nenhuma', 'Cinza', 'Preto', 'OW_Herobrine'),
('Montanha', 120, 5, 'Neve', 'Verde Escuro', 'Azul Claro', 'OW_Miner'), ('Savana', 70, 28, 'Nenhuma', 'Amarelo Claro', 'Azul', 'OW_Builder'),
('Selva', 75, 25, 'Chuva', 'Verde Vívido', 'Azul Esverdeado', 'OW_Explorer'), ('Praia', 64, 22, 'Chuva', 'Verde', 'Azul Turquesa', 'OW_Warrior'),
('Pântano', 62, 18, 'Chuva', 'Verde Oliva', 'Marrom', 'OW_Farmer'), ('Colinas', 90, 12, 'Neve', 'Verde', 'Azul', 'OW_Enchanter');

-- Catálogo de itens, receitas e ingredientes (vêm antes dos slots, que usam esses itens)
INSERT INTO TIPO_ITEM (Nome, Dano_Base, Área_de_Ataque, Repulsão, Pilha_Máxima, Raridade) VALUES
('Tronco', 0, 0, 0, 64, 'Comum'), ('Tábua', 0, 0, 0, 64, 'Comum'), ('Graveto', 0, 0, 0, 64, 'Comum'),
('Pedra Lapidada', 0, 0, 0, 64, 'Comum'), ('Pedra', 0, 0, 0, 64, 'Comum'), ('Carvão', 0, 0, 0, 64, 'Comum'),
('Areia', 0, 0, 0, 64, 'Comum'), ('Vidro', 0, 0, 0, 64, 'Comum'), ('Argila', 0, 0, 0, 64, 'Comum'),
('Tijolo', 0, 0, 0, 64, 'Comum'), ('Linha', 0, 0, 0, 64, 'Comum'), ('Trigo', 0, 0, 0, 64, 'Comum'),
('Minério de Ferro Bruto', 0, 0, 0, 64, 'Comum'), ('Lingote de Ferro', 0, 0, 0, 64, 'Comum'),
('Minério de Ouro Bruto', 0, 0, 0, 64, 'Incomum'), ('Lingote de Ouro', 0, 0, 0, 64, 'Incomum'),
('Diamante', 0, 0, 0, 64, 'Raro'), ('Lingote de Netherita', 0, 0, 0, 64, 'Épico'),
('Pão', 0, 0, 0, 64, 'Comum'), ('Batata', 0, 0, 0, 64, 'Comum'), ('Batata Assada', 0, 0, 0, 64, 'Comum'),
('Carne Crua', 0, 0, 0, 64, 'Comum'), ('Bife', 0, 0, 0, 64, 'Comum'), ('Peixe Cru', 0, 0, 0, 64, 'Comum'),
('Peixe Cozido', 0, 0, 0, 64, 'Comum'), ('Bancada', 0, 0, 0, 64, 'Comum'), ('Fornalha', 0, 0, 0, 64, 'Comum'),
('Alto-forno', 0, 0, 0, 64, 'Comum'), ('Defumador', 0, 0, 0, 64, 'Comum'), ('Baú', 0, 0, 0, 64, 'Comum'),
('Tocha', 0, 0, 0, 64, 'Comum'), ('Placa de Madeira', 0, 0, 0, 64, 'Comum'), ('Degrau de Pedra', 0, 0, 0, 64, 'Comum'),
('Picareta de Pedra', 3, 1, 0, 1, 'Comum'), ('Picareta de Ferro', 4, 1, 0, 1, 'Comum'),
('Machado de Ferro', 9, 1, 1, 1, 'Comum'), ('Espada de Ferro', 6, 2, 1, 1, 'Comum'),
('Espada de Diamante', 7, 2, 1, 1, 'Raro'), ('Espada de Netherita', 8, 2, 1, 1, 'Épico'),
('Arco', 6, 0, 1, 1, 'Comum'), ('Capacete de Ferro', 0, 0, 0, 1, 'Comum'), ('Peitoral de Ferro', 0, 0, 0, 1, 'Comum');

INSERT INTO TIPO_ITEM_CONSUMÍVEL (Nome, Lançável, Fome_recuperada) VALUES
('Pão', false, 5), ('Batata', false, 1), ('Batata Assada', false, 5), ('Carne Crua', false, 3),
('Bife', false, 8), ('Peixe Cru', false, 2), ('Peixe Cozido', false, 5);

INSERT INTO TIPO_ITEM_DESGASTÁVEL (Nome, Durabilidade, Equipável) VALUES
('Picareta de Pedra', 131, true), ('Picareta de Ferro', 250, true), ('Machado de Ferro', 250, true),
('Espada de Ferro', 250, true), ('Espada de Diamante', 1561, true), ('Espada de Netherita', 2031, true),
('Arco', 384, true), ('Capacete de Ferro', 165, true), ('Peitoral de Ferro', 240, true);

INSERT INTO ITEM_CLASSE (Classe_Item, Nome) VALUES
('Material', 'Tronco'), ('Material', 'Tábua'), ('Material', 'Graveto'), ('Material', 'Pedra Lapidada'),
('Material', 'Pedra'), ('Material', 'Carvão'), ('Material', 'Areia'), ('Material', 'Vidro'),
('Material', 'Argila'), ('Material', 'Tijolo'), ('Material', 'Linha'), ('Material', 'Trigo'),
('Material', 'Minério de Ferro Bruto'), ('Material', 'Lingote de Ferro'), ('Material', 'Minério de Ouro Bruto'),
('Material', 'Lingote de Ouro'), ('Material', 'Diamante'), ('Material', 'Lingote de Netherita'),
('Alimento', 'Pão'), ('Alimento', 'Batata'), ('Alimento', 'Batata Assada'), ('Alimento', 'Carne Crua'),
('Alimento', 'Bife'), ('Alimento', 'Peixe Cru'), ('Alimento', 'Peixe Cozido'), ('Bloco', 'Bancada'),
('Bloco', 'Fornalha'), ('Bloco', 'Alto-forno'), ('Bloco', 'Defumador'), ('Bloco', 'Baú'),
('Bloco', 'Tocha'), ('Bloco', 'Placa de Madeira'), ('Bloco', 'Degrau de Pedra'),
('Ferramenta', 'Picareta de Pedra'), ('Ferramenta', 'Picareta de Ferro'), ('Ferramenta', 'Machado de Ferro'),
('Arma', 'Espada de Ferro'), ('Arma', 'Espada de Diamante'), ('Arma', 'Espada de Netherita'),
('Arma', 'Arco'), ('Armadura', 'Capacete de Ferro'), ('Armadura', 'Peitoral de Ferro');

INSERT INTO RECEITA_CRAFTING (Receita, Tipo_de_Crafting, Tempo_para_o_Crafting, Item_Resultado, Quantidade_Resultado) VALUES
('Receita_Tábua', 'Bancada', NULL, 'Tábua', 4), ('Receita_Graveto', 'Bancada', NULL, 'Graveto', 4),
('Receita_Bancada', 'Bancada', NULL, 'Bancada', 1), ('Receita_Fornalha', 'Bancada', NULL, 'Fornalha', 1),
('Receita_Baú', 'Bancada', NULL, 'Baú', 1), ('Receita_Tocha', 'Bancada', NULL, 'Tocha', 4),
('Receita_Placa_Madeira', 'Bancada', NULL, 'Placa de Madeira', 3), ('Receita_Picareta_Pedra', 'Bancada', NULL, 'Picareta de Pedra', 1),
('Receita_Picareta_Ferro', 'Bancada', NULL, 'Picareta de Ferro', 1), ('Receita_Machado_Ferro', 'Bancada', NULL, 'Machado de Ferro', 1),
('Receita_Espada_Ferro', 'Bancada', NULL, 'Espada de Ferro', 1), ('Receita_Espada_Diamante', 'Bancada', NULL, 'Espada de Diamante', 1),
('Receita_Arco', 'Bancada', NULL, 'Arco', 1), ('Receita_Capacete_Ferro', 'Bancada', NULL, 'Capacete de Ferro', 1),
('Receita_Armadura_Ferro', 'Bancada', NULL, 'Peitoral de Ferro', 1), ('Receita_Pão', 'Bancada', NULL, 'Pão', 1),
('Receita_Alto_Forno', 'Bancada', NULL, 'Alto-forno', 1), ('Receita_Defumador', 'Bancada', NULL, 'Defumador', 1),
('Receita_Ferro_Lingote', 'Fornalha', 10, 'Lingote de Ferro', 1), ('Receita_Ouro_Lingote', 'Fornalha', 10, 'Lingote de Ouro', 1),
('Receita_Vidro', 'Fornalha', 10, 'Vidro', 1), ('Receita_Pedra', 'Fornalha', 10, 'Pedra', 1),
('Receita_Tijolo', 'Fornalha', 10, 'Tijolo', 1), ('Receita_Carvão', 'Fornalha', 10, 'Carvão', 1),
('Receita_Batata_Assada', 'Fornalha', 10, 'Batata Assada', 1), ('Receita_Bife_Fornalha', 'Fornalha', 10, 'Bife', 1),
('Receita_Ferro_Lingote_Alto_Forno', 'Alto-forno', 5, 'Lingote de Ferro', 1), ('Receita_Ouro_Lingote_Alto_Forno', 'Alto-forno', 5, 'Lingote de Ouro', 1),
('Receita_Bife_Defumador', 'Defumador', 5, 'Bife', 1), ('Receita_Peixe_Cozido_Defumador', 'Defumador', 5, 'Peixe Cozido', 1),
('Receita_Bife_Fogueira', 'Fogueira', 30, 'Bife', 1), ('Receita_Peixe_Cozido_Fogueira', 'Fogueira', 30, 'Peixe Cozido', 1),
('Receita_Degrau_Pedra', 'Cortador de Pedra', NULL, 'Degrau de Pedra', 2), ('Receita_Espada_Netherita', 'Mesa de Ferraria', NULL, 'Espada de Netherita', 1);

INSERT INTO CRAFTING_ITEM (Posição_Slot, Quantidade, Item, Receita, Combustível) VALUES
(1, 1, 'Tronco', 'Receita_Tábua', false), (1, 1, 'Tábua', 'Receita_Graveto', false), (4, 1, 'Tábua', 'Receita_Graveto', false),
(1, 1, 'Tábua', 'Receita_Bancada', false), (2, 1, 'Tábua', 'Receita_Bancada', false), (4, 1, 'Tábua', 'Receita_Bancada', false),
(5, 1, 'Tábua', 'Receita_Bancada', false), (1, 1, 'Pedra Lapidada', 'Receita_Fornalha', false),
(2, 1, 'Pedra Lapidada', 'Receita_Fornalha', false), (3, 1, 'Pedra Lapidada', 'Receita_Fornalha', false),
(4, 1, 'Pedra Lapidada', 'Receita_Fornalha', false), (6, 1, 'Pedra Lapidada', 'Receita_Fornalha', false),
(7, 1, 'Pedra Lapidada', 'Receita_Fornalha', false), (8, 1, 'Pedra Lapidada', 'Receita_Fornalha', false),
(9, 1, 'Pedra Lapidada', 'Receita_Fornalha', false), (1, 1, 'Tábua', 'Receita_Baú', false),
(2, 1, 'Tábua', 'Receita_Baú', false), (3, 1, 'Tábua', 'Receita_Baú', false), (4, 1, 'Tábua', 'Receita_Baú', false),
(6, 1, 'Tábua', 'Receita_Baú', false), (7, 1, 'Tábua', 'Receita_Baú', false), (8, 1, 'Tábua', 'Receita_Baú', false),
(9, 1, 'Tábua', 'Receita_Baú', false), (2, 1, 'Carvão', 'Receita_Tocha', false), (5, 1, 'Graveto', 'Receita_Tocha', false),
(1, 1, 'Tábua', 'Receita_Placa_Madeira', false), (2, 1, 'Tábua', 'Receita_Placa_Madeira', false),
(3, 1, 'Tábua', 'Receita_Placa_Madeira', false), (4, 1, 'Tábua', 'Receita_Placa_Madeira', false),
(5, 1, 'Tábua', 'Receita_Placa_Madeira', false), (6, 1, 'Tábua', 'Receita_Placa_Madeira', false),
(8, 1, 'Graveto', 'Receita_Placa_Madeira', false), (1, 1, 'Pedra Lapidada', 'Receita_Picareta_Pedra', false),
(2, 1, 'Pedra Lapidada', 'Receita_Picareta_Pedra', false), (3, 1, 'Pedra Lapidada', 'Receita_Picareta_Pedra', false),
(5, 1, 'Graveto', 'Receita_Picareta_Pedra', false), (8, 1, 'Graveto', 'Receita_Picareta_Pedra', false),
(1, 1, 'Lingote de Ferro', 'Receita_Picareta_Ferro', false), (2, 1, 'Lingote de Ferro', 'Receita_Picareta_Ferro', false),
(3, 1, 'Lingote de Ferro', 'Receita_Picareta_Ferro', false), (5, 1, 'Graveto', 'Receita_Picareta_Ferro', false),
(8, 1, 'Graveto', 'Receita_Picareta_Ferro', false), (1, 1, 'Lingote de Ferro', 'Receita_Machado_Ferro', false),
(2, 1, 'Lingote de Ferro', 'Receita_Machado_Ferro', false), (4, 1, 'Lingote de Ferro', 'Receita_Machado_Ferro', false),
(5, 1, 'Graveto', 'Receita_Machado_Ferro', false), (8, 1, 'Graveto', 'Receita_Machado_Ferro', false),
(2, 1, 'Lingote de Ferro', 'Receita_Espada_Ferro', false), (5, 1, 'Lingote de Ferro', 'Receita_Espada_Ferro', false),
(8, 1, 'Graveto', 'Receita_Espada_Ferro', false), (2, 1, 'Diamante', 'Receita_Espada_Diamante', false),
(5, 1, 'Diamante', 'Receita_Espada_Diamante', false), (8, 1, 'Graveto', 'Receita_Espada_Diamante', false),
(2, 1, 'Graveto', 'Receita_Arco', false), (4, 1, 'Graveto', 'Receita_Arco', false), (8, 1, 'Graveto', 'Receita_Arco', false),
(3, 1, 'Linha', 'Receita_Arco', false), (6, 1, 'Linha', 'Receita_Arco', false), (9, 1, 'Linha', 'Receita_Arco', false),
(1, 1, 'Lingote de Ferro', 'Receita_Capacete_Ferro', false), (2, 1, 'Lingote de Ferro', 'Receita_Capacete_Ferro', false),
(3, 1, 'Lingote de Ferro', 'Receita_Capacete_Ferro', false), (4, 1, 'Lingote de Ferro', 'Receita_Capacete_Ferro', false),
(6, 1, 'Lingote de Ferro', 'Receita_Capacete_Ferro', false), (1, 1, 'Lingote de Ferro', 'Receita_Armadura_Ferro', false),
(3, 1, 'Lingote de Ferro', 'Receita_Armadura_Ferro', false), (4, 1, 'Lingote de Ferro', 'Receita_Armadura_Ferro', false),
(5, 1, 'Lingote de Ferro', 'Receita_Armadura_Ferro', false), (6, 1, 'Lingote de Ferro', 'Receita_Armadura_Ferro', false),
(7, 1, 'Lingote de Ferro', 'Receita_Armadura_Ferro', false), (8, 1, 'Lingote de Ferro', 'Receita_Armadura_Ferro', false),
(9, 1, 'Lingote de Ferro', 'Receita_Armadura_Ferro', false), (1, 1, 'Trigo', 'Receita_Pão', false),
(2, 1, 'Trigo', 'Receita_Pão', false), (3, 1, 'Trigo', 'Receita_Pão', false),
(1, 1, 'Lingote de Ferro', 'Receita_Alto_Forno', false), (2, 1, 'Lingote de Ferro', 'Receita_Alto_Forno', false),
(3, 1, 'Lingote de Ferro', 'Receita_Alto_Forno', false), (5, 1, 'Fornalha', 'Receita_Alto_Forno', false),
(7, 1, 'Pedra', 'Receita_Alto_Forno', false), (8, 1, 'Pedra', 'Receita_Alto_Forno', false),
(9, 1, 'Pedra', 'Receita_Alto_Forno', false), (2, 1, 'Tronco', 'Receita_Defumador', false),
(4, 1, 'Tronco', 'Receita_Defumador', false), (6, 1, 'Tronco', 'Receita_Defumador', false),
(8, 1, 'Tronco', 'Receita_Defumador', false), (5, 1, 'Fornalha', 'Receita_Defumador', false),
(1, 1, 'Minério de Ferro Bruto', 'Receita_Ferro_Lingote', false), (2, 1, 'Carvão', 'Receita_Ferro_Lingote', true),
(1, 1, 'Minério de Ouro Bruto', 'Receita_Ouro_Lingote', false), (2, 1, 'Carvão', 'Receita_Ouro_Lingote', true),
(1, 1, 'Areia', 'Receita_Vidro', false), (2, 1, 'Carvão', 'Receita_Vidro', true),
(1, 1, 'Pedra Lapidada', 'Receita_Pedra', false), (2, 1, 'Carvão', 'Receita_Pedra', true),
(1, 1, 'Argila', 'Receita_Tijolo', false), (2, 1, 'Carvão', 'Receita_Tijolo', true),
(1, 1, 'Tronco', 'Receita_Carvão', false), (2, 1, 'Tábua', 'Receita_Carvão', true),
(1, 1, 'Batata', 'Receita_Batata_Assada', false), (2, 1, 'Carvão', 'Receita_Batata_Assada', true),
(1, 1, 'Carne Crua', 'Receita_Bife_Fornalha', false), (2, 1, 'Carvão', 'Receita_Bife_Fornalha', true),
(1, 1, 'Minério de Ferro Bruto', 'Receita_Ferro_Lingote_Alto_Forno', false), (2, 1, 'Carvão', 'Receita_Ferro_Lingote_Alto_Forno', true),
(1, 1, 'Minério de Ouro Bruto', 'Receita_Ouro_Lingote_Alto_Forno', false), (2, 1, 'Carvão', 'Receita_Ouro_Lingote_Alto_Forno', true),
(1, 1, 'Carne Crua', 'Receita_Bife_Defumador', false), (2, 1, 'Carvão', 'Receita_Bife_Defumador', true),
(1, 1, 'Peixe Cru', 'Receita_Peixe_Cozido_Defumador', false), (2, 1, 'Carvão', 'Receita_Peixe_Cozido_Defumador', true),
(1, 1, 'Carne Crua', 'Receita_Bife_Fogueira', false), (1, 1, 'Peixe Cru', 'Receita_Peixe_Cozido_Fogueira', false),
(1, 1, 'Pedra', 'Receita_Degrau_Pedra', false), (1, 1, 'Espada de Diamante', 'Receita_Espada_Netherita', false),
(2, 1, 'Lingote de Netherita', 'Receita_Espada_Netherita', false);

INSERT INTO SLOT_INVENTÁRIO (Número_Slot, Inventário, Quantidade, Mostrar_Durabilidade_atual, Item) VALUES
(0, 1, 1, 0, 'Espada de Ferro'), (0, 2, 64, 0, 'Tábua'), (0, 3, 1, 0, 'Picareta de Pedra'),
(0, 4, 1, 0, 'Picareta de Ferro'), (0, 5, 1, 0, 'Espada de Diamante'), (0, 6, 12, 0, 'Pão'),
(0, 7, 5, 0, 'Bife'), (0, 8, 3, 0, 'Batata Assada'), (0, 9, 1, 0, 'Arco'), (0, 10, 1, 0, 'Capacete de Ferro');

INSERT INTO TIPO_BLOCO (Nome, Durabilidade, Condição_de_Quebra, Hitbox, Dropável, Interagível, Quebrável, Coletável, Número_Slot, Inventário) VALUES
('Pedra', 50, 1, 1, true, false, true, true, 0, 1), ('Terra', 10, 0, 1, true, false, true, true, 0, 2),
('Madeira', 30, 1, 1, true, false, true, true, 0, 3), ('Areia', 5, 0, 1, true, false, true, true, 0, 4),
('Minério de Ferro', 60, 2, 1, true, false, true, true, 0, 5), ('Minério de Ouro', 60, 2, 1, true, false, true, true, 0, 6),
('Diamante', 100, 3, 1, true, false, true, true, 0, 7), ('Obsidiana', 500, 4, 1, true, false, true, true, 0, 8),
('Vidro', 5, 0, 1, true, true, true, true, 0, 9), ('Baú', 50, 1, 1, true, true, true, true, 0, 10);

INSERT INTO DOMESTICAÇÃO_MOB (Data_Domesticação, Name_Tag, Coordenadas, Jogador, Mob) VALUES
('2024-01-05', 'Mimosa', 100, 'Farmer09', 'Vaca'), ('2024-01-06', 'Bacon', 101, 'Farmer09', 'Porco'),
('2024-01-07', 'Fofinha', 102, 'Builder06', 'Ovelha'), ('2024-01-08', 'Trovão', 103, 'Explorer07', 'Cavalo'),
('2024-01-09', 'Miau', 104, 'Steve01', 'Gato'), ('2024-02-01', 'Rex', 105, 'Warrior08', 'Lobo'),
('2024-02-02', 'Algodão', 106, 'Farmer09', 'Ovelha'), ('2024-02-03', 'Sombra', 107, 'Miner05', 'Gato'),
('2024-02-04', NULL, 108, 'Notch03', 'Cavalo'), ('2024-02-05', 'Fenrir', 109, 'Alex02', 'Lobo');

INSERT INTO TIPO_MOB_PACÍFICO (Nome, Domesticável, Comportamento_de_Fuga, Montável) VALUES
('Vaca', true, true, false), ('Porco', true, true, false), ('Ovelha', true, true, false),
('Cavalo', true, true, true), ('Gato', true, true, false);

INSERT INTO TIPO_MOB_HOSTIL (Nome, Sensibilidade_ao_Sol, Spawn_no_escuro, Barra_de_Vida_Visível, É_Boss) VALUES
('Zumbi', true, true, false, false), ('Esqueleto', true, true, false, false), ('Creeper', false, true, false, false),
('Aranha', false, true, false, false), ('Bruxa', false, true, false, false);

INSERT INTO TIPO_MOB_NEUTRO (Nome, Sofreu_Ataque, Domesticável) VALUES
('Enderman', false, false), ('Lobo', true, true), ('Piglin', false, false), ('Abelha', false, false), ('Panda', false, false);

INSERT INTO TIPO_ESTRUTURA (Nome, Variante, Extensão, Bioma) VALUES
('Vila', 'Planície', 50, 'Planície'), ('Vila', 'Deserto', 45, 'Deserto'), ('Vila', 'Savana', 48, 'Savana'),
('Templo', 'Deserto', 20, 'Deserto'), ('Templo', 'Selva', 25, 'Selva'), ('Mansão', 'Floresta', 80, 'Floresta'),
('Fortaleza', 'Caverna Escura', 100, 'Caverna Escura'), ('Iglu', 'Montanha', 10, 'Montanha'),
('Naufrágio', 'Praia', 15, 'Praia'), ('Cabana_Pantano', 'Pântano', 12, 'Pântano');

INSERT INTO ENTIDADE_DINÂMICA (Nome, Data_de_Criação, Quebrável, Hitbox, Item) VALUES
('Item_Dropado_1', '2024-03-01', true, 1, 'Diamante'), ('Item_Dropado_2', '2024-03-02', true, 1, 'Carvão'),
('Item_Dropado_3', '2024-03-03', true, 1, 'Pão'), ('Item_Dropado_4', '2024-03-04', true, 1, 'Espada de Ferro'),
('Item_Dropado_5', '2024-03-05', true, 1, 'Tocha'), ('Item_Dropado_6', '2024-03-06', true, 1, 'Vidro'),
('Item_Dropado_7', '2024-03-07', true, 1, 'Tábua'), ('Item_Dropado_8', '2024-03-08', true, 1, 'Bife'),
('Item_Dropado_9', '2024-03-09', true, 1, 'Areia'), ('Item_Dropado_10', '2024-03-10', true, 1, 'Tijolo');

INSERT INTO INVENTÁRIO_JOGADOR (id_inventário, Slot_hotbar_selecionado) VALUES
(1, 0), (2, 1), (3, 2), (4, 3), (5, 4);

INSERT INTO INVENTÁRIO_BAÚ (Tipo_Baú, Expansível, Coordenadas_Baú, Dimensão, Nome) VALUES
(11, false, 200, 'OW_Steve', 'OW_Steve'), (12, true, 201, 'OW_Alex', 'OW_Alex'),
(13, false, 202, 'OW_Notch', 'OW_Notch'), (14, true, 203, 'OW_Herobrine', 'OW_Herobrine'),
(15, false, 204, 'OW_Miner', 'OW_Miner');

INSERT INTO DIMENSÃO_PORTAL (Dimensão, Tipo_do_Portal, Coordenadas) VALUES
('OW_Steve', 'Portal do Nether', 300), ('OW_Alex', 'Portal do End', 301),
('OW_Notch', 'Portal do Nether', 302), ('OW_Herobrine', 'Portal do End', 303),
('OW_Miner', 'Portal do Nether', 304);

INSERT INTO GERAÇÃO_MOB_DIMENSÃO (Mob, Dimensão, Taxa_de_Spawn) VALUES
('Zumbi', 'OW_Steve', 10), ('Esqueleto', 'OW_Alex', 8), ('Creeper', 'OW_Notch', 5),
('Enderman', 'OW_Herobrine', 15), ('Vaca', 'OW_Miner', 20);

INSERT INTO GERAÇãO_BLOCO_BIOMA (Bioma, Bloco, Taxa_de_Geração) VALUES
('Floresta', 'Madeira', 100), ('Deserto', 'Areia', 90), ('Planície', 'Terra', 80),
('Montanha', 'Minério de Ferro', 30), ('Caverna Escura', 'Diamante', 20),
('Montanha', 'Pedra', 100), ('Colinas', 'Pedra', 70), ('Caverna Escura', 'Minério de Ouro', 15),
('Caverna Escura', 'Obsidiana', 5), ('Selva', 'Madeira', 100), ('Savana', 'Terra', 70),
('Praia', 'Areia', 100), ('Pântano', 'Terra', 60), ('Floresta', 'Terra', 60);

INSERT INTO GERAÇÃO_MOB_BIOMA (Mob, Bioma, Taxa_de_Spawn) VALUES
('Zumbi', 'Floresta', 25), ('Esqueleto', 'Caverna Escura', 20), ('Creeper', 'Montanha', 15),
('Vaca', 'Planície', 30), ('Aranha', 'Caverna Escura', 10),
('Porco', 'Planície', 20), ('Ovelha', 'Planície', 20), ('Cavalo', 'Savana', 20), ('Vaca', 'Savana', 10),
('Aranha', 'Selva', 20), ('Creeper', 'Selva', 12), ('Bruxa', 'Pântano', 18), ('Aranha', 'Pântano', 10),
('Zumbi', 'Deserto', 15), ('Esqueleto', 'Deserto', 10), ('Zumbi', 'Praia', 12), ('Gato', 'Praia', 5),
('Ovelha', 'Colinas', 25), ('Lobo', 'Colinas', 15), ('Lobo', 'Floresta', 12), ('Aranha', 'Floresta', 15),
('Esqueleto', 'Montanha', 10);

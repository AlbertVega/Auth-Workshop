import bcrypt
import pymysql

#Este script hashea las contras que ya estan en la DB.


# Conecta como en tu app
conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="", # Reemplaza con tu contraseña
    database="ejercicio_auth",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with conn.cursor() as cur:
        # Paso 1: Agregar columna password_hash si no existe
        print("1️⃣  Agregando columna password_hash...")
        try:
            cur.execute("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)")
            conn.commit()
            print("   ✓ Columna agregada")
        except pymysql.err.OperationalError as e:
            if "1060" in str(e):  # Error de columna duplicada
                print("   ℹ️  Columna ya existe")
            else:
                raise
        
        # Paso 2: Obtener los usuarios con contraseña en claro
        print("\n2️⃣  Leyendo usuarios con contraseñas en claro...")
        cur.execute("SELECT id, email, password_plain FROM users WHERE password_plain IS NOT NULL")
        users = cur.fetchall()
        print(f"   ✓ {len(users)} usuarios encontrados")
        
        # Paso 3: Hashear cada contraseña
        print("\n3️⃣  Hasheando contraseñas (esto demora)...")
        for user in users:
            user_id = user['id']
            email = user['email']
            password_plain = user['password_plain']
            
            # Hashea (rounds=12 es estándar)
            hashed = bcrypt.hashpw(password_plain.encode('utf-8'), bcrypt.gensalt(rounds=12))
            hashed_str = hashed.decode('utf-8')
            
            cur.execute("UPDATE users SET password_hash = %s WHERE id = %s", 
                        (hashed_str, user_id))
            print(f"   ✓ {email}: {hashed_str[:20]}...")
        
        conn.commit()
        
        # Paso 4 (opcional): Borrar la columna vieja
        print("\n4️⃣  Borrando columna password_plain...")
        cur.execute("ALTER TABLE users DROP COLUMN password_plain")
        conn.commit()
        print("   ✓ Columna borrada")
        
        print("\n✅ Migración completada")

finally:
    conn.close()
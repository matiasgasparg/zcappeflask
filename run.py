from app import init_app

if __name__ == "__main__":
    # Inicializar la aplicación Flask
    app = init_app()
    
    # Ejecutar la aplicación Flask en todas las direcciones IP en el puerto 5000
    app.run(host='0.0.0.0', port=5000)

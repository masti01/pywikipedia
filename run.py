from app import app


if app.config['ENV'] == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')
    
#print(f"CONFIG:{app.config['ENV']}")
print(f"CONFIG (RUN):{app.config}")


if __name__ == "__main__":
    app.run()
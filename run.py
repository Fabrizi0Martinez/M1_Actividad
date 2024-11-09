from cleaning_model import CleaningModel

def main():
    model = CleaningModel(15, 20, 20, 0.7, 100)
    model.run_model()

if __name__ == "__main__":
    main()
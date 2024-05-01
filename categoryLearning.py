import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import os

from utils import evaluate_model, create_training_directory
from wrangling import videos
from torch.utils.data import random_split


class ThumbnailDataset(Dataset):
    def __init__(self, dataframe, transform=None):
        """
        Args:
            dataframe (pandas.DataFrame): DataFrame containing the URLs and labels.
            transform (callable, optional): Optional transform to be applied on a sample.
        """
        self.dataframe = dataframe
        self.transform = transform

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        img_url = self.dataframe.iloc[idx]['thumbnail']
        category = self.dataframe.iloc[idx]['categoryId']
        # Download the image
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        # Apply transformations
        if self.transform:
            img = self.transform(img)
        return img, category


transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize the image to fit the model input size
    transforms.ToTensor(),  # Convert image to PyTorch Tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Normalization
])
dataset = ThumbnailDataset(videos, transform=transform)
total_size = len(dataset)
val_size = int(total_size * 0.1)
train_size = total_size - val_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=4, shuffle=False)

model = resnet18(pretrained=True)
num_classes = videos['categoryId'].max()
print("number of classes: " + str(num_classes))
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
num_epochs = 10
print('Training on ' + str(device))
# Training loop
for epoch in range(num_epochs):
    path = create_training_directory('./loggings')
    model.train()
    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.long().to(device)

        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # Evaluate the model
    accuracy = evaluate_model(model, val_loader, device)
    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}, Accuracy: {accuracy:.4f}')

    # Save the model after each epoch
    torch.save(model.state_dict(), os.path.join(path, 'model state ' + str(epoch)))


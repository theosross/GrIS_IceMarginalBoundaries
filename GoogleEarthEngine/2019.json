// Script to classify 2019 Landsat collection in Greenland

// Load countries polygons
var lsib = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017");
// Filter to only Greenland
var country = lsib.filterMetadata('country_na','equals','Greenland');

// Load a Landsat ImageCollection for July-August 2019.
var collection_2019 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
    .filterDate('2019-07-01', '2019-08-31')
    .filterBounds(country)
    .filter(ee.Filter.lt('CLOUD_COVER', 20))
    .median();
    
var visParamsTrue = {bands: ['B4', 'B3', 'B2'], min: 0, max: 2500, gamma: 1.1};

Map.centerObject(country,3);
Map.addLayer(collection_2019, visParamsTrue, 'Landsat 2019');

// Create training data
var training = water.merge(ice).merge(land);

var label = 'type';
var bands = ['B2','B3','B4','B5','B6'];
var input = collection_2019.select(bands);

var trainImage = input.sampleRegions({
  collection: training,
  properties: [label],
  scale: 30
});

var trainingData = trainImage.randomColumn();
var trainSet = trainingData.filter(ee.Filter.lessThan('random', 0.8));
var testSet = trainingData.filter(ee.Filter.greaterThanOrEquals('random', 0.8));

// Classification Model
var classifier = ee.Classifier.smileRandomForest(10).train(trainingData, label, bands);

// Define collection that will be classified
var input_2019 = collection_2019.select(bands);

// Classify the image
var classified = input_2019.classify(classifier);
var classified = classified.uint8();

var landcoverPalette = [
  '0099FF', // Water (0)
  'FFFFFF', // Ice (1)
  '008302', // Land (2)
];

// Add classified and edge layers
Map.addLayer(classified, {palette: landcoverPalette, min:0, max:2}, 'Classified');

// Accuracy Assesment
var confusionMatrix = ee.ConfusionMatrix(testSet.classify(classifier)
  .errorMatrix({
    actual: 'type',
    predicted: 'classification'
  }));

print('Confusion Matrix:', confusionMatrix);
print('Overall Accuracy:', confusionMatrix.accuracy());

/*
// Export classified image
Export.image.toDrive({
  image: classified,
  description: 'Landsat_Greenland_2019',
  scale: 30,
  region: country,
  maxPixels: 1e13
});


var imageRGB = collection_2019.visualize({bands: ['B4', 'B3', 'B2'], min: 0, max: 2500});
print("rgb",imageRGB);

Map.addLayer(imageRGB, {min:0, max:2500, gamma:1.1},'rgb');

// Export rgb image
Export.image.toDrive({
  image: imageRGB,
  description: '2019_rgb',  
  scale: 30,  
  region: geometry3,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13,
  crs: 'EPSG:3413'
});

var band5 = collection_2019.select('B5');
var band6 = collection_2019.select('B6');

// Export band 5 and 6 image
Export.image.toDrive({
  image: band5,
  description: '2019_Band5',  
  scale: 30,  
  region: geometry3,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13,
  crs: 'EPSG:3413'
});

Export.image.toDrive({
  image: band6,
  description: '2019_Band6',  
  scale: 30,  
  region: geometry3,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13,
  crs: 'EPSG:3413'
});
*/
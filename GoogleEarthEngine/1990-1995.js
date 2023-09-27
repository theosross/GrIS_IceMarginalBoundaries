// Load countries polygons
var lsib = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017");
// Filter to only Greenland
var country = lsib.filterMetadata('country_na','equals','Greenland');

var filterSummer = ee.Filter.or(
    ee.Filter.date('1990-07-01', '1990-08-31'),
    ee.Filter.date('1991-07-01', '1991-08-31'),
    ee.Filter.date('1992-07-01', '1992-08-31'),
    ee.Filter.date('1993-07-01', '1993-08-31'),
    ee.Filter.date('1994-07-01', '1994-08-31'),
    ee.Filter.date('1995-07-01', '1995-08-31')
);

// Applies scaling factors.
function applyScaleFactors(image) {
  var opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);
  var thermalBand = image.select('ST_B6').multiply(0.00341802).add(149.0);
  return image.addBands(opticalBands, null, true)
              .addBands(thermalBand, null, true);
}


// Load a Landsat ImageCollection for July-August 2010.
var collection_1990 = ee.ImageCollection("LANDSAT/LT05/C02/T1_L2")
    .filterBounds(country)
    .filter(filterSummer)
    .filter(ee.Filter.lt('CLOUD_COVER', 20));

collection_1990 = collection_1990.map(applyScaleFactors);

var collection_1990 = collection_1990.median();
    
var visualization = {
  bands: ['SR_B3', 'SR_B2', 'SR_B1'],
  min: 0.0,
  max: 0.3
};

Map.centerObject(country,3);
Map.addLayer(collection_1990, visualization, 'Landsat 1990');

// Create training data
var training = water.merge(ice).merge(land);

var label = 'type';
var bands = ['SR_B1','SR_B2','SR_B3','SR_B4','SR_B5','SR_B7'];
var input = collection_1990.select(bands);

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
var input_1990 = collection_1990.select(bands);

// Classify the image
var classified = input_1990.classify(classifier);
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

var band4 = collection_1990.select('SR_B4');

/*

// Export rgb image
Export.image.toDrive({
  image: band4,
  description: '1990_Band4',  
  scale: 30,  
  region: geometry,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13,
  crs: 'EPSG:3413'
});

var imageRGB = collection_1990.visualize({bands: ['SR_B3', 'SR_B2', 'SR_B1'], min: 0.0, max: 0.3});
print("rgb",imageRGB);

// Export rgb image
Export.image.toDrive({
  image: imageRGB,
  description: '1990_RGB',  
  scale: 30,  
  region: geometry3,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13,
  crs: 'EPSG:3413'
});


// Export classified image
Export.image.toDrive({
  image: classified,
  description: 'Landsat_Greenland_1990',
  scale: 30,
  region: country,
  maxPixels: 1e13
});
*/
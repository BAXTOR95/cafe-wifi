'use strict';

// Define CONFIGURATION globally but initialize it after fetching
let CONFIGURATION;

// Define constants for address components
const SHORT_NAME_ADDRESS_COMPONENT_TYPES = new Set([
	'street_number',
	'administrative_area_level_1',
	'postal_code',
]);

const ADDRESS_COMPONENT_TYPES_IN_FORM = [
	'location',
	'locality',
	'administrative_area_level_1',
	'postal_code',
	'country',
];

let activeFilters = {
	'has-wifi': false,
	'has-sockets': false,
	'has-toilet': false,
	'can-take-calls': false,
};

function updateMapCenter(element) {
	var latitude = parseFloat(element.getAttribute('data-latitude'));
	var longitude = parseFloat(element.getAttribute('data-longitude'));
	const mapElement = document.getElementById('cafemap');

	mapElement.setAttribute('center', `${latitude},${longitude}`);
}

function toggleFilter(filter) {
	// Toggle the state of the filter
	activeFilters[filter] = !activeFilters[filter];

	// Update the appearance of the filter icon
	const filterIcon = document.getElementById(`${filter}-icon`);
	if (activeFilters[filter]) {
		filterIcon.classList.add('filter-active');
	} else {
		filterIcon.classList.remove('filter-active');
	}

	// Filter the listings based on the active filters
	var listings = document.querySelectorAll('.listing-card');
	listings.forEach((listing) => {
		let display = true;
		for (const key in activeFilters) {
			if (activeFilters[key]) {
				// Use backticks for template literals to correctly interpolate the key
				const attributeValue = listing.getAttribute(`data-${key}`);
				if (attributeValue !== 'True') {
					display = false;
					break;
				}
			}
		}
		// Apply the determined display state to the listing
		listing.style.display = display ? '' : 'none';
		// Ensure the d-flex class is correctly added or removed based on the display state
		if (display) {
			listing.classList.add('d-flex');
		} else {
			listing.classList.remove('d-flex');
		}
	});
}

// Utility functions for handling address form inputs and place data
function getFormInputElement(componentType) {
	return document.getElementById(`${componentType}_input`);
}

function fillInAddress(place) {
	function getComponentName(componentType) {
		for (const component of place.address_components || []) {
			if (component.types[0] === componentType) {
				return SHORT_NAME_ADDRESS_COMPONENT_TYPES.has(componentType)
					? component.short_name
					: component.long_name;
			}
		}
		return '';
	}

	function getComponentText(componentType) {
		return componentType === 'location'
			? `${getComponentName('street_number')} ${getComponentName('route')}`
			: getComponentName(componentType);
	}

	for (const componentType of ADDRESS_COMPONENT_TYPES_IN_FORM) {
		getFormInputElement(componentType).value = getComponentText(componentType);
	}
}

function renderAddress(place, map, marker) {
	if (place.geometry && place.geometry.location) {
		map.panTo(place.geometry.location);
		marker.position = place.geometry.location;
	} else {
		marker.position = null;
	}
}

// Initialize map and related components after configuration is loaded
async function initApplication() {
	const { Map } = await google.maps.importLibrary('maps');
	const { AdvancedMarkerElement } = await google.maps.importLibrary('marker');
	const { Autocomplete } = await google.maps.importLibrary('places');
	const mapOptions = CONFIGURATION.mapOptions;

	// Check if the element for the gmp-map exists
	if (document.getElementById('gmp-map')) {
		mapOptions.mapId = mapOptions.mapId || 'ADD_CAFE_MAP_ID';
		mapOptions.center = mapOptions.center || { lat: 37.4221, lng: -122.0841 };

		const map = new Map(document.getElementById('gmp-map'), mapOptions);
		const marker = new AdvancedMarkerElement({ map });
		const autocomplete = new Autocomplete(getFormInputElement('location'), {
			fields: ['address_components', 'geometry', 'name'],
			types: ['address'],
		});

		autocomplete.addListener(
			'place_changed',
			() => {
				const place = autocomplete.getPlace();
				if (!place.geometry) {
					window.alert(`No details available for input: '${place.name}'`);
					return;
				}
				renderAddress(place, map, marker);
				fillInAddress(place);
			},
			{ passive: true },
		);
	}
}

// Fetch configuration from the server and initialize the application
fetch('/config')
	.then((response) => response.json())
	.then((config) => {
		CONFIGURATION = {
			ctaTitle: 'Add',
			mapOptions: {
				center: { lat: 37.4221, lng: -122.0841 },
				fullscreenControl: true,
				mapTypeControl: false,
				streetViewControl: true,
				zoom: 11,
				zoomControl: true,
				maxZoom: 22,
				mapId: 'gmp-map',
			},
			mapsApiKey: config.mapsApiKey,
			capabilities: {
				addressAutocompleteControl: true,
				mapDisplayControl: true,
				ctaControl: true,
			},
		};

		// Initialize the application after CONFIGURATION is ready
		initApplication();
	});

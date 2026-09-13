# CHANGELOG

## Version 1.0
Release date: 2026-09-04

### Overview
Version 1.0 marks the first stable release of the World Culinary Map. The application provides an interactive world map that groups countries into culinary regions and presents characteristic information about each cuisine.

---

## Added

### Interactive World Map
- Interactive SVG-based world map.
- All regions are displayed directly within the page.
- Responsive layout within the map container.
- Stable browser-based implementation without external map libraries.

### Culinary Region Classification
Implemented culinary regions for:

#### Europe
- Balkan
- Oost-Centraal Europa
- Scandinavië
- Britse Eilanden
- Germaanse Wereld
- Midden-Europa
- Mediterrane Wereld

#### Midden-Oosten
- Anatolië
- Levant
- Perzische Wereld
- Arabisch Schiereiland

#### Azië
- Rusland & Eurazië
- Kaukasus
- Centraal-Azië
- China & Oost-Azië
- Japan
- Indochina
- Maleis-Indonesische Wereld
- Filipijnen
- Zuid-Azië

#### Afrika
- Maghreb
- Nijlvallei
- Sahel
- West-Afrika
- Hoorn van Afrika
- Centraal-Afrika
- Oost-Afrika
- Zuidelijk Afrika

#### Noord-Amerika
- Canada
- Verenigde Staten

#### Latijns-Amerika
- Mexico
- Centraal-Amerika
- Caribisch Gebied
- Andes
- Brazilië
- Amazone & Guyana's
- Pampas

#### Oceanië
- Australië
- Nieuw-Zeeland
- Melanesië
- Polynesië
- Micronesië

---

## Region Information Panel

Added dynamic information panel containing:

- Region title
- Culinary description
- Characteristic ingredients

Information updates automatically when hovering over a culinary region.

---

## Visual Design

### Region Colour System
- Unique colour palette for all culinary regions.
- Consistent colour families per continent.
- Improved visual distinction between continents.
- Hover effect uses darker shades of the original region colour.

### Layout
- Two-column layout:
  - Interactive map
  - Information sidebar
- Fixed-height information box to prevent layout shifting.
- Improved visual balance between map and sidebar.
- Region image support implemented.

---

## Interaction

### Hover Behaviour
- Whole culinary region highlights on hover.
- Region information is displayed automatically.
- Colours return to their original state when leaving a region.

### Country Mapping
- Support for SVG regions identified by:
  - id
  - name
  - class
- Automatic matching of countries to culinary regions.
- Full coverage of all supported regions in the SVG world map.

---

## Technical Improvements

### SVG Integration
- SVG embedded directly in HTML.
- Removed dependency on external SVG object loading.
- Eliminated cross-origin and contentDocument issues.

### Code Cleanup
- Removed obsolete continent navigation.
- Removed page redirection logic.
- Removed zoom and viewBox navigation functionality.
- Removed continent-specific page dependencies.

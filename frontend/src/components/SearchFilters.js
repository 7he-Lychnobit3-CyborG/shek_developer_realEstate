import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter, X } from 'lucide-react';

const SearchFilters = ({ onSearch, initialFilters = {} }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [filters, setFilters] = useState({
    query: '',
    property_type: '',
    status: '',
    min_price: '',
    max_price: '',
    min_bedrooms: '',
    max_bedrooms: '',
    min_bathrooms: '',
    max_bathrooms: '',
    city: '',
    state: '',
    min_area: '',
    max_area: '',
    is_featured: '',
    ...initialFilters,
  });

  const propertyTypes = [
    { value: '', label: 'Any Type' },
    { value: 'apartment', label: 'Apartment' },
    { value: 'house', label: 'House' },
    { value: 'villa', label: 'Villa' },
    { value: 'commercial', label: 'Commercial' },
    { value: 'land', label: 'Land' },
  ];

  const statusOptions = [
    { value: '', label: 'Any Status' },
    { value: 'for_sale', label: 'For Sale' },
    { value: 'for_rent', label: 'For Rent' },
  ];

  const handleInputChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSearch = () => {
    // Filter out empty values
    const cleanFilters = Object.entries(filters).reduce((acc, [key, value]) => {
      if (value !== '' && value !== null && value !== undefined) {
        acc[key] = value;
      }
      return acc;
    }, {});

    onSearch(cleanFilters);
  };

  const handleReset = () => {
    const resetFilters = {
      query: '',
      property_type: '',
      status: '',
      min_price: '',
      max_price: '',
      min_bedrooms: '',
      max_bedrooms: '',
      min_bathrooms: '',
      max_bathrooms: '',
      city: '',
      state: '',
      min_area: '',
      max_area: '',
      is_featured: '',
    };
    setFilters(resetFilters);
    onSearch({});
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
      {/* Basic Search */}
      <div className="flex flex-col md:flex-row gap-4 mb-4">
        <div className="flex-1">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <input
              type="text"
              placeholder="Search by location, title, or description..."
              value={filters.query}
              onChange={(e) => handleInputChange('query', e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        <select
          value={filters.property_type}
          onChange={(e) => handleInputChange('property_type', e.target.value)}
          className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          {propertyTypes.map(type => (
            <option key={type.value} value={type.value}>{type.label}</option>
          ))}
        </select>

        <select
          value={filters.status}
          onChange={(e) => handleInputChange('status', e.target.value)}
          className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          {statusOptions.map(status => (
            <option key={status.value} value={status.value}>{status.label}</option>
          ))}
        </select>

        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200"
        >
          <Filter className="h-5 w-5 mr-2" />
          Filters
        </button>

        <button
          onClick={handleSearch}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 font-medium"
        >
          Search
        </button>
      </div>

      {/* Advanced Filters */}
      <motion.div
        initial={false}
        animate={{
          height: isExpanded ? 'auto' : 0,
          opacity: isExpanded ? 1 : 0,
        }}
        transition={{ duration: 0.3 }}
        className="overflow-hidden"
      >
        <div className="border-t pt-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
            {/* Price Range */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Price Range</label>
              <div className="flex space-x-2">
                <input
                  type="number"
                  placeholder="Min"
                  value={filters.min_price}
                  onChange={(e) => handleInputChange('min_price', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <input
                  type="number"
                  placeholder="Max"
                  value={filters.max_price}
                  onChange={(e) => handleInputChange('max_price', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Bedrooms */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Bedrooms</label>
              <div className="flex space-x-2">
                <input
                  type="number"
                  placeholder="Min"
                  value={filters.min_bedrooms}
                  onChange={(e) => handleInputChange('min_bedrooms', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <input
                  type="number"
                  placeholder="Max"
                  value={filters.max_bedrooms}
                  onChange={(e) => handleInputChange('max_bedrooms', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Bathrooms */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Bathrooms</label>
              <div className="flex space-x-2">
                <input
                  type="number"
                  placeholder="Min"
                  value={filters.min_bathrooms}
                  onChange={(e) => handleInputChange('min_bathrooms', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <input
                  type="number"
                  placeholder="Max"
                  value={filters.max_bathrooms}
                  onChange={(e) => handleInputChange('max_bathrooms', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Area */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Area (sqft)</label>
              <div className="flex space-x-2">
                <input
                  type="number"
                  placeholder="Min"
                  value={filters.min_area}
                  onChange={(e) => handleInputChange('min_area', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <input
                  type="number"
                  placeholder="Max"
                  value={filters.max_area}
                  onChange={(e) => handleInputChange('max_area', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            {/* Location */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">City</label>
              <input
                type="text"
                placeholder="Enter city"
                value={filters.city}
                onChange={(e) => handleInputChange('city', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">State</label>
              <input
                type="text"
                placeholder="Enter state"
                value={filters.state}
                onChange={(e) => handleInputChange('state', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Featured */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Featured Properties Only</label>
              <select
                value={filters.is_featured}
                onChange={(e) => handleInputChange('is_featured', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Properties</option>
                <option value="true">Featured Only</option>
              </select>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-end space-x-3">
            <button
              onClick={handleReset}
              className="flex items-center px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors duration-200"
            >
              <X className="h-4 w-4 mr-2" />
              Reset
            </button>
            <button
              onClick={handleSearch}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 font-medium"
            >
              Apply Filters
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default SearchFilters;
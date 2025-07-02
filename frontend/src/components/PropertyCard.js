import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Heart, MapPin, Bed, Bath, Square, Eye } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { favoritesAPI } from '../services/api';
import toast from 'react-hot-toast';

const PropertyCard = ({ property, onFavoriteChange }) => {
  const [isFavorited, setIsFavorited] = useState(false);
  const [loading, setLoading] = useState(false);
  const { isAuthenticated } = useAuth();

  const handleFavoriteClick = async (e) => {
    e.preventDefault();
    
    if (!isAuthenticated) {
      toast.error('Please login to add favorites');
      return;
    }

    setLoading(true);
    try {
      if (isFavorited) {
        await favoritesAPI.remove(property.id);
        setIsFavorited(false);
        toast.success('Removed from favorites');
      } else {
        await favoritesAPI.add(property.id);
        setIsFavorited(true);
        toast.success('Added to favorites');
      }
      
      if (onFavoriteChange) {
        onFavoriteChange(property.id, !isFavorited);
      }
    } catch (error) {
      toast.error('Error updating favorites');
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      for_sale: { label: 'For Sale', color: 'bg-green-100 text-green-800' },
      for_rent: { label: 'For Rent', color: 'bg-blue-100 text-blue-800' },
      sold: { label: 'Sold', color: 'bg-gray-100 text-gray-800' },
      rented: { label: 'Rented', color: 'bg-purple-100 text-purple-800' },
    };
    
    return statusConfig[status] || { label: status, color: 'bg-gray-100 text-gray-800' };
  };

  const status = getStatusBadge(property.status);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      whileHover={{ y: -5 }}
      className="bg-white rounded-lg shadow-lg overflow-hidden group"
    >
      <Link to={`/properties/${property.id}`}>
        <div className="relative">
          {/* Property Image */}
          <div className="h-64 bg-gray-300 overflow-hidden">
            {property.images && property.images.length > 0 ? (
              <img
                src={property.images[0]}
                alt={property.title}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              />
            ) : (
              <div className="w-full h-full bg-gradient-to-br from-gray-300 to-gray-400 flex items-center justify-center">
                <span className="text-gray-600 text-lg">No Image</span>
              </div>
            )}
          </div>

          {/* Status Badge */}
          <div className="absolute top-4 left-4">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${status.color}`}>
              {status.label}
            </span>
          </div>

          {/* Featured Badge */}
          {property.is_featured && (
            <div className="absolute top-4 right-4">
              <span className="px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
                Featured
              </span>
            </div>
          )}

          {/* Favorite Button */}
          <button
            onClick={handleFavoriteClick}
            disabled={loading}
            className="absolute bottom-4 right-4 p-2 bg-white rounded-full shadow-md hover:shadow-lg transition-shadow duration-200"
          >
            <Heart
              className={`h-5 w-5 ${
                isFavorited ? 'text-red-500 fill-current' : 'text-gray-400'
              } ${loading ? 'animate-pulse' : ''}`}
            />
          </button>
        </div>

        {/* Property Details */}
        <div className="p-6">
          {/* Price and Property Type */}
          <div className="flex justify-between items-start mb-2">
            <h3 className="text-2xl font-bold text-gray-900">
              {formatPrice(property.price)}
              {property.status === 'for_rent' && <span className="text-base font-normal text-gray-600">/month</span>}
            </h3>
            <span className="text-sm text-gray-500 capitalize">
              {property.property_type.replace('_', ' ')}
            </span>
          </div>

          {/* Title */}
          <h4 className="text-lg font-semibold text-gray-800 mb-2 line-clamp-2">
            {property.title}
          </h4>

          {/* Location */}
          <div className="flex items-center text-gray-600 mb-4">
            <MapPin className="h-4 w-4 mr-1" />
            <span className="text-sm">
              {property.address}, {property.city}, {property.state}
            </span>
          </div>

          {/* Property Features */}
          <div className="flex items-center justify-between text-gray-600 mb-4">
            <div className="flex items-center space-x-4">
              <div className="flex items-center">
                <Bed className="h-4 w-4 mr-1" />
                <span className="text-sm">{property.bedrooms}</span>
              </div>
              <div className="flex items-center">
                <Bath className="h-4 w-4 mr-1" />
                <span className="text-sm">{property.bathrooms}</span>
              </div>
              <div className="flex items-center">
                <Square className="h-4 w-4 mr-1" />
                <span className="text-sm">{property.area_sqft.toLocaleString()} sqft</span>
              </div>
            </div>
            
            <div className="flex items-center text-gray-500">
              <Eye className="h-4 w-4 mr-1" />
              <span className="text-sm">{property.views || 0}</span>
            </div>
          </div>

          {/* Description */}
          <p className="text-gray-600 text-sm line-clamp-2 mb-4">
            {property.description}
          </p>

          {/* Amenities */}
          {property.amenities && property.amenities.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {property.amenities.slice(0, 3).map((amenity, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
                >
                  {amenity}
                </span>
              ))}
              {property.amenities.length > 3 && (
                <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                  +{property.amenities.length - 3} more
                </span>
              )}
            </div>
          )}
        </div>
      </Link>
    </motion.div>
  );
};

export default PropertyCard;
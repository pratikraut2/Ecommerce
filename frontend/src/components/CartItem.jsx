import React from "react";

const CartItem = ({ item, onUpdateQuantity, onRemove }) => {
  return (
    <div className="cart-item">
      {/* Product Image */}
      <img
        src={item.product.image || "/assets/no-image.png"}
        alt={item.product.name}
        className="cart-item-img"
      />

      {/* Product Info */}
      <div className="cart-item-info">
        <h3>{item.product.name}</h3>
        <p>Price: ₹{item.product.price}</p>

        {/* Quantity Controls */}
        <div className="cart-item-quantity">
          <button
            onClick={() => onUpdateQuantity(item.product.id, item.quantity - 1)}
            disabled={item.quantity <= 1}
          >
            -
          </button>
          <span>{item.quantity}</span>
          <button
            onClick={() => onUpdateQuantity(item.product.id, item.quantity + 1)}
          >
            +
          </button>
        </div>

        <p>Total: ₹{item.product.price * item.quantity}</p>
      </div>

      {/* Remove Button */}
      <button className="remove-btn" onClick={() => onRemove(item.product.id)}>
        ❌
      </button>
    </div>
  );
};

export default CartItem;

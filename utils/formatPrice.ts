export default function formatPrice(price = 0) {
  return `${(price / 1000).toFixed(2)}€/kWh`;
}

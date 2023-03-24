// Date() => "24 de marzo, 2023"
export const formatDate = (date: Date) => {
  return `${date.getDate()} de ${date.toLocaleString("es", {
    month: "long",
  })}, ${date.getFullYear()}`;
};

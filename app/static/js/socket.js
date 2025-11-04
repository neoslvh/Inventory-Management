const socket = io();
socket.on('connect', () => console.log('socket connected'));
socket.on('stock_updated', payload => {
console.log('stock_updated', payload);
});
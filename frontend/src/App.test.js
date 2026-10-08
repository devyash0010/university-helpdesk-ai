import { render, screen, fireEvent, act } from '@testing-library/react';
import App from './App';

// jsdom does not provide WebSocket or fetch, so stub both.
class MockWebSocket {
  constructor() {
    this.readyState = 1;
  }
  send() {}
  close() {}
}

global.WebSocket = MockWebSocket;
global.fetch = () =>
  Promise.resolve({ json: () => Promise.resolve([]) });

beforeEach(() => {
  localStorage.clear();
});

test('renders the chat launcher widget', async () => {
  render(<App />);
  await act(async () => {});
  expect(screen.getByText('💬')).toBeInTheDocument();
});

test('opens the chat panel with a greeting when the widget is clicked', async () => {
  render(<App />);
  await act(async () => {});
  fireEvent.click(screen.getByText('💬'));

  expect(screen.getByText('🎓 University Helpdesk')).toBeInTheDocument();
  expect(
    screen.getByText(/Hi 👋 I'm your University Helpdesk Assistant/i)
  ).toBeInTheDocument();
  expect(screen.getByPlaceholderText('Ask your issue...')).toBeInTheDocument();
});


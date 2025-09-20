import React, { useState } from 'react';
import styled, { createGlobalStyle } from 'styled-components';

// Global styles
const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
      'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
      sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background-color: #f5f5f5;
    color: #2c2c2c;
    line-height: 1.6;
  }
`;

// Styled components
const AppContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
`;

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
`;

const Header = styled.header`
  background: linear-gradient(135deg, #00a651 0%, #7ed321 100%);
  color: white;
  padding: 20px 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
`;

const Logo = styled.div`
  h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 5px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }
`;

const Subtitle = styled.span`
  font-size: 1.1rem;
  opacity: 0.9;
  font-weight: 300;
`;

const Main = styled.main`
  flex: 1;
  padding: 40px 0;
`;

const SearchSection = styled.div`
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
  border: 1px solid #e0e0e0;

  h2 {
    color: #2c2c2c;
    margin-bottom: 25px;
    font-size: 1.8rem;
    font-weight: 600;
  }
`;

const InputGroup = styled.div`
  display: flex;
  gap: 15px;
  align-items: center;

  @media (max-width: 768px) {
    flex-direction: column;
    gap: 15px;
  }
`;

const SearchInput = styled.input`
  flex: 1;
  padding: 15px 20px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  background: white;

  &:focus {
    outline: none;
    border-color: #00a651;
    box-shadow: 0 0 0 3px rgba(0, 166, 81, 0.1);
  }

  &:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
  }
`;

const SearchButton = styled.button`
  background: linear-gradient(135deg, #00a651 0%, #7ed321 100%);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(0, 166, 81, 0.3);

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 166, 81, 0.4);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  @media (max-width: 768px) {
    width: 100%;
  }
`;

const Loading = styled.div`
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
`;

const Spinner = styled.div`
  width: 40px;
  height: 40px;
  border: 4px solid #e0e0e0;
  border-top: 4px solid #00a651;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const Error = styled.div`
  background: #fee;
  color: #c33;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #fcc;
  margin-bottom: 30px;
  text-align: center;
`;

const ResultsSection = styled.div`
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
  border: 1px solid #e0e0e0;

  h3 {
    color: #2c2c2c;
    margin-bottom: 20px;
    font-size: 1.5rem;
    font-weight: 600;
  }
`;

const HighlightedText = styled.div`
  background: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  font-size: 1.2rem;
  line-height: 1.8;
  margin-bottom: 25px;
  border: 1px solid #e0e0e0;
  min-height: 60px;
`;

const Entity = styled.span<{ entityType: string; isBeginning: boolean }>`
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
  margin: 0 1px;
  display: inline-block;
  position: relative;
  background: ${props => props.isBeginning ? '#00a651' : '#7ed321'};
  color: white;
`;

const EntitiesList = styled.div`
  h4 {
    color: #2c2c2c;
    margin-bottom: 15px;
    font-size: 1.2rem;
    font-weight: 600;
  }

  ul {
    list-style: none;
    display: grid;
    gap: 10px;
  }
`;

const EntityItem = styled.li`
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px 15px;
  background: #f5f5f5;
  border-radius: 6px;
  border: 1px solid #e0e0e0;

  @media (max-width: 768px) {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
`;

const EntityText = styled.span`
  font-weight: 600;
  color: #2c2c2c;
  flex: 1;
`;

const EntityType = styled.span`
  background: #00a651;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 500;
`;

const EntityPosition = styled.span`
  color: #666666;
  font-size: 0.9rem;
  font-family: monospace;
`;

const Footer = styled.footer`
  background: #2c2c2c;
  color: white;
  padding: 20px 0;
  text-align: center;
  margin-top: auto;

  p {
    opacity: 0.8;
    font-size: 0.9rem;
  }
`;

interface Entity {
  start_index: number;
  end_index: number;
  entity: string;
}

const App: React.FC = () => {
  const [input, setInput] = useState('');
  const [entities, setEntities] = useState<Entity[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!input.trim()) return;

    setLoading(true);
    setError(null);
    setEntities([]);

    try {
      const response = await fetch('http://localhost:3001/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input: input.trim() }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setEntities(data.entities || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Произошла ошибка');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const renderHighlightedText = () => {
    if (!input || entities.length === 0) return input;

    const parts: React.ReactNode[] = [];
    let lastIndex = 0;

    entities
      .sort((a, b) => a.start_index - b.start_index)
      .forEach((entity, index) => {
        // Добавляем текст до сущности
        if (entity.start_index > lastIndex) {
          parts.push(
            <span key={`text-${index}`}>
              {input.slice(lastIndex, entity.start_index)}
            </span>
          );
        }

        // Добавляем выделенную сущность
        const entityText = input.slice(entity.start_index, entity.end_index);
        const entityType = entity.entity.replace(/^[BI]-/, '');
        const isBeginning = entity.entity.startsWith('B-');
        
        parts.push(
          <Entity
            key={`entity-${index}`}
            entityType={entityType}
            isBeginning={isBeginning}
            title={`${entityType}: ${entityText}`}
          >
            {entityText}
          </Entity>
        );

        lastIndex = entity.end_index;
      });

    // Добавляем оставшийся текст
    if (lastIndex < input.length) {
      parts.push(
        <span key="text-end">
          {input.slice(lastIndex)}
        </span>
      );
    }

    return parts;
  };

  return (
    <AppContainer>
      <GlobalStyle />
      <Header>
        <Container>
          <Logo>
            <h1>Пятёрочка</h1>
            <Subtitle>NER - Поиск товаров</Subtitle>
          </Logo>
        </Container>
      </Header>

      <Main>
        <Container>
          <SearchSection>
            <h2>Введите запрос для поиска товаров</h2>
            <InputGroup>
              <SearchInput
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Например: сгущенное молоко, хлеб бородинский, сыр российский"
                disabled={loading}
              />
              <SearchButton
                onClick={handleSearch}
                disabled={loading || !input.trim()}
              >
                {loading ? 'Поиск...' : 'Найти товары'}
              </SearchButton>
            </InputGroup>
          </SearchSection>

          {loading && (
            <Loading>
              <Spinner />
              <p>Анализируем запрос...</p>
            </Loading>
          )}

          {error && (
            <Error>
              <p>❌ {error}</p>
            </Error>
          )}

          {entities.length > 0 && (
            <ResultsSection>
              <h3>Результаты поиска:</h3>
              <HighlightedText>
                {renderHighlightedText()}
              </HighlightedText>
              <EntitiesList>
                <h4>Найденные сущности:</h4>
                <ul>
                  {entities.map((entity, index) => {
                    const entityText = input.slice(entity.start_index, entity.end_index);
                    const entityType = entity.entity.replace(/^[BI]-/, '');
                    return (
                      <EntityItem key={index}>
                        <EntityText>{entityText}</EntityText>
                        <EntityType>{entityType}</EntityType>
                        <EntityPosition>
                          {entity.start_index}-{entity.end_index}
                        </EntityPosition>
                      </EntityItem>
                    );
                  })}
                </ul>
              </EntitiesList>
            </ResultsSection>
          )}
        </Container>
      </Main>

      <Footer>
        <Container>
          <p>© 2025 Пятёрочка. Система поиска товаров с использованием NER</p>
        </Container>
      </Footer>
    </AppContainer>
  );
};

export default App;

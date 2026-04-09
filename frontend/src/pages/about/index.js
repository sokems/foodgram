import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'

const About = ({ updateOrders, orders }) => {
  
  return <Main>
    <MetaTags>
      <title>О проекте</title>
      <meta name="description" content="Фудграм - О проекте" />
      <meta property="og:title" content="О проекте" />
    </MetaTags>
    
    <Container>
      <h1 className={styles.title}>Добро пожаловать!</h1>
      <div className={styles.content}>
        <div>
          <h2 className={styles.subtitle}>О чём этот проект?</h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
             Это Фудграм — платформа для любителей кулинарии, созданная в рамках обучения в Яндекс Практикуме. Проект разработан с нуля и представляет собой полноценное веб-приложение.
            </p>
            <p className={styles.textItem}>
             Здесь вы можете делиться своими рецептами, находить вдохновение в рецептах других пользователей, добавлять понравившиеся блюда в избранное и составлять список покупок для приготовления блюд из выбранных рецептов.
            </p>
            <p className={styles.textItem}>
             Для доступа ко всем функциям сайта необходима регистрация. E-mail не проходит проверку, поэтому вы можете использовать любой адрес для создания аккаунта.
            </p>
            <p className={styles.textItem}>
              Заходите и делитесь своими любимыми рецептами!
            </p>
          </div>
        </div>
        <aside>
          <h2 className={styles.additionalTitle}>
            Ссылки
          </h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
              Исходный код проекта доступен на{' '}
                  <a href="https://github.com/AVKharkova/foodgram" className={styles.textLink}>
                    Github
                  </a>
            </p>
            <p className={styles.textItem}>
              Автор проекта:{' '}
                  <a href="https://github.com/AVKharkova" className={styles.textLink}>
                    Анастасия Харькова
                  </a>
            </p>
          </div>
        </aside>
      </div>
      
    </Container>
  </Main>
}

export default About


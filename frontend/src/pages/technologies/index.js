import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'

const Technologies = () => {
  return (
    <Main>
      <MetaTags>
        <title>Технологии</title>
        <meta name="description" content="Фудграм - Технологии проекта" />
        <meta property="og:title" content="Технологии" />
      </MetaTags>

      <Container>
        <h1 className={styles.title}>Технологии проекта</h1>
        <div className={styles.content}>
          <div>
            <h2 className={styles.subtitle}>Какие технологии использованы в Фудграм:</h2>
            <div className={styles.text}>
              <ul className={styles.textItem}>
                <li className={styles.textItem}>Python</li>
                <li className={styles.textItem}>Django</li>
                <li className={styles.textItem}>Django REST Framework</li>
                <li className={styles.textItem}>Djoser</li>
                <li className={styles.textItem}>PostgreSQL</li>
                <li className={styles.textItem}>React</li>
                <li className={styles.textItem}>Docker</li>
                <li className={styles.textItem}>Gunicorn</li>
                <li className={styles.textItem}>Nginx</li>
              </ul>
            </div>
          </div>
          <aside>
            <h2 className={styles.additionalTitle}>Полезные ссылки</h2>
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
  )
}

export default Technologies
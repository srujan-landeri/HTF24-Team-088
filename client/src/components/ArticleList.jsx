import ArticleCard from "./ArticleCard";


// ArticleList component
const ArticleList = ({ articles, onLike, onDislike }) => {
  return (
    <div className="space-y-6">
      {articles.map((article, index) => (
        <ArticleCard
          key={index}
          article={article}
          onLike={onLike}
          onDislike={onDislike}
        />
      ))}
    </div>
  );
};

export default ArticleList;
import "@toast-ui/editor/dist/toastui-editor.css";
import { Editor } from "@toast-ui/react-editor";
import ExitImg from "assets/img/exit.svg";
import WriteLayout from "components/layouts/WriteLayout";
import { useEffect, useRef, useState } from "react";
import { Button, Col, Form, Image, Row } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { useAuthStore } from "stores/RootStore";
import { customAxios } from "util/CustomAxios";


const InsertPost = () => {
  // // 정규표현식을 이용한 태그 제거
  // const markdownImageRegex = /\[.*\]\((.*)\)/gi;
  // const markdownRegex = /(\*|_|#|`|~|>|!|\[|\]|\(|\)|\{|\}|\||\\)/gi;

  const refs = useRef({
    title: null,
    /** @type {Editor} editor */
    editor: null,
  });

  const authStore = useAuthStore();
  const navigate = useNavigate();


  const [editorHeight, setEditorHeight] = useState(0);

  // 임시저장
  const tempPostSave = () => {
    const tempPost = {
      title : refs.current.title.value,
      content : refs.current.editor.getInstance().getMarkdown()
    }
    localStorage.setItem("tempPost", JSON.stringify(tempPost));
    alert("임시저장되었습니다.")
  };

  // 임시저장 불러오기
  const tempPostCheck = () => {
    const tempPost = localStorage.getItem("tempPost");
    if(tempPost != null) {
      if(window.confirm("임시저장된 글이 있습니다. 불러오시겠습니까?")){
        const parsedTempPost = JSON.parse(tempPost);
        refs.current.title.value = parsedTempPost.title;
        refs.current.editor.getInstance().setMarkdown(parsedTempPost.content);
      }
    } else {
      localStorage.removeItem("tempPost");
    }
  }

  // 유효성 체크 / 통신하기 전에 미리 확인하는 것이 좋다.
  const validateFields = () => {
    const title = refs.current.title.value;
    const content = refs.current.editor.getInstance().getMarkdown();

    if (title === "") {
      alert("제목을 입력하세요.");
      return false;
    }
    if (content === "") {
      alert("내용을 입력하세요.");
      return false;
    }

    return true;
  };

  // 게시하기
  const insertPost = () => {
    if(!validateFields()) {
      return;
    }

    const title = refs.current.title.value;
    const content = refs.current.editor.getInstance().getMarkdown();

    // 정규표현식을 이용한 태그 제거
    const markdownImageRegex = /\[.*\]\((.*)\)/gi;
    const markdownRegex = /(\*|_|#|`|~|>|!|\[|\]|\(|\)|\{|\}|\||\\)/gi;

    const summary = content
      .replace(markdownImageRegex, "")
      .replace(markdownImageRegex, "")
      .substring(0, 151);  // 151은 포함되지 않음

    const imageList = content.match(markdownImageRegex);
    const thumbnailMarkdown = imageList != null ? imageList[0] : null;

    const thumbnail =
      thumbnailMarkdown != null? thumbnailMarkdown.substring(
        thumbnailMarkdown.indexOf("](") + 2,
        thumbnailMarkdown.length - 1
      ) : null;

    const newPost = {
      title : title,
      thumbnail: thumbnail,
      content : content,
      summary: summary,
    };

    customAxios
    .privateAxios({
      method: `post`,
      url: `/api/v1/posts`,
      data: newPost,
    })
    .then((response) => {
      if (response.status === 201) {
        alert("게시하였습니다.");
        navigate(`/post/${response.data.content.idx}`, {replace: true});
      } else {
        alert(response.data.message);
      }
    })
    .catch((error) => {
      const detail = error?.response?.data?.detail;
      if (detail != null) {
        alert(JSON.stringify(detail));
      } else {
        alert("오류가 발생했습니다. 관리자에게 문의하세요.");
      }
    })
    .finally(() => {});

  };

  // useEffect(() => {}, [])


  useEffect(() => {
    if(authStore.loginUser != null) {
      refs.current.editor.getInstance().setMarkdown("");
      setEditorHeight(`${window.innerHeight - 190}px`);
      window.onresize = () => setEditorHeight(`${window.innerHeight - 190}px`);
      tempPostCheck();
    }
  }, [authStore]);

  // 로그인 확인: 로그인 상태확인해서 로그인페이지로 이동시키기
  useEffect(() => {
    if(authStore.loginUser === null) {
      alert("로그인이 필요합니다.");
      navigate("/login", { replace: true});
    }
  }, [authStore, navigate]);

  // if (authStore.loginUser == null) {
  //   return <div>로딩 중</div>;
  // }

  return (
    <WriteLayout>
      <Row>
        <Col>
          <Form.Control
            ref={(el) => (refs.current.title = el)}
            className="border-0 w-100 fs-1 mt-3 mb-3"
            type="text"
            placeholder="제목을 입력하세요"
          />
        </Col>
      </Row>
      <Editor
        ref={(el) => (refs.current.editor = el)}
        previewStyle="vertical"
        initialEditType="markdown"
        height={editorHeight}
      />
      <Row className="row fixed-bottom p-3 bg-white shadow-lg">
        <Col className="me-auto">
          <Link to={-1} className="text-decoration-none text-dark">
            <Image src={ExitImg} />
            <span className="m-2">나가기</span>
          </Link>
        </Col>
        <Col className="col-auto">
          <Button className="btn-light fw-bold" type="button" onClick={tempPostSave}>
            임시저장
          </Button>
        </Col>
        <Col className="col-auto">
          <Button
            className="btn-light fw-bold text-white"
            type="button"
            style={{ backgroundColor: "#20c997" }}
            onClick={insertPost}
          >
            게시하기
          </Button>
        </Col>
      </Row>
    </WriteLayout>
  );
};

export default InsertPost;
